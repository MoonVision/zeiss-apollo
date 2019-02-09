from collections import defaultdict

import torch
from torch.utils.data import DataLoader
import torch.nn.functional as F
from torchvision.datasets import ImageFolder

from vision.data_prep import get_label, stratified_split, DataSubSet
from vision.models import torchvision_default_initialize_weights


def loss_hinge(result_sum, min_sum:float = 2000, max_sum:float = 6000):
    loss = F.relu(result_sum - max_sum) + \
           F.relu(-result_sum + min_sum)
    return loss

def run_epoch(ds, m, optimizer, epoch_nr=0, num_workers=0, batch_size=4,
              debug_print=True, debug_plot=True, train=True,
              TRUTH_BOUNDS={"NO FEATURE": (0, 100 // 4),
                            "COMPLETE FEATURE": (900 // 4, 2000 // 4),
                            "BORDERTOUCHER": (500 // 4, 1800 // 4)}):
    if train:
        m.train()
    else:
        m.eval()

    dl = DataLoader(ds)
    device = next(m.parameters()).device

    losses = []
    sums = defaultdict(list)  # How many pixels are active for each class

    for b, (imgs, classes) in enumerate(dl):
        if train:
            optimizer.zero_grad()

        imgs = imgs.to(device)
        preds = m(imgs)
        preds = F.softmax(preds, dim=2)

        single_losses = []
        for pred, _cls in zip(preds, classes):
            s = pred.sum()

            label = get_label(ds, _cls.item())
            lower, upper = TRUTH_BOUNDS[label]
            l = loss_hinge(s, lower, upper) / ((lower + upper) * 0.5)
            single_losses.append(l)

            sums[label].append(s.item())

        loss = sum(single_losses)
        if train:
            loss.backward()
            optimizer.step()

        if debug_print:
            labels = [get_label(ds, k.item()) for k in classes]
            print(
                f"E[{epoch_nr}]-train {b}: {loss:.2f}, shapes: {[i.shape for i in imgs]}, labels: {labels}")

        losses.append(loss.item())

    if debug_plot:
        import matplotlib.pyplot as plt

        for label, v in sums.items():
            plt.plot(sorted(v), ".", label=label)
        plt.legend()
        plt.title("TRAIN" if train else "EVAL")

    return losses


if __name__=="__main__":

    import argparse
    import importlib

    from torchvision.transforms import Compose
    from torchvision import transforms

    parser = argparse.ArgumentParser(description='ZEISS Lab training')

    parser.add_argument("-e", "--epochs", default=20, type=int)
    parser.add_argument("-d", "--debug-print", action="store_true")
    parser.add_argument("-m", "--model", default="SlimWide")
    opt = parser.parse_args()


    tf_eval = Compose([transforms.Grayscale(), transforms.ToTensor(),
                       transforms.Normalize((0.4862745,), (0.1388,)), ])

    tf_train = Compose(
            [transforms.Grayscale(), transforms.RandomHorizontalFlip(),
             transforms.RandomVerticalFlip(), transforms.ToTensor(),
             transforms.Normalize((0.4862745,), (0.1388,)), ])

    ds = ImageFolder('photomask_trainingdata')
    eval_idx, train_idx = stratified_split([x[1] for x in ds.samples])

    ds_eval = DataSubSet(ds, eval_idx, transform=tf_eval)
    ds_train = DataSubSet(ds, train_idx, transform=tf_train)

    ModelClass = getattr(importlib.import_module("vision.models"), opt.model)
    m = ModelClass()
    torchvision_default_initialize_weights(m)

    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    m.to(device)

    print("Model loaded:", opt.model)
    optimizer = torch.optim.SGD(m.parameters(), lr=1e-5, momentum=0.9,
                                weight_decay=1e-4)
    epoch_nr = 0

    print("Data train", len(ds_train), "Data eval", len(ds_eval))
    while epoch_nr <= opt.epochs:
        losses = run_epoch(ds_train, m, optimizer, epoch_nr=epoch_nr, train=True,
                           debug_print=opt.debug_print, debug_plot=False)

        print(f"E[{epoch_nr}] AVERAGE train:", sum(losses) / len(losses))

        eval_losses = run_epoch(ds_eval, m, optimizer, epoch_nr=epoch_nr,
                                train=False, debug_print=False, debug_plot=False)
        print(f"E[{epoch_nr}] AVERAGE eval:", sum(eval_losses) / len(eval_losses))

        epoch_nr += 1