import React, { useState, useEffect, useRef, Fragment } from 'react';
import moment from 'moment';
import Plot from 'react-plotly.js';

import api from 'js/api'
import Card from "components/CardList/Card"
import CardList from "components/CardList/CardList"

function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  });

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}

export default function Home() {
  const [latestImage, setLatestImage] = useState();

  useInterval(async () => {
    const response = await api.get('/defectpositionimages/?limit=1')
    if (response.data.count > 0 &&
       (!latestImage || response.data.results[0].id !== latestImage.id)) {
      setLatestImage(response.data.results[0]);
    }
  }, 250);


  const [masksOverview, setMasksOverivew] = useState();
  useInterval(async () => {
    const response = await api.get('/masks/overview/')
    setMasksOverivew(response.data);
  }, 250);

  return (
    <div>
      <CardList>
        <Card>
          <h3>Latest Image</h3>
          {latestImage ?
            <Fragment>
              <img src={latestImage.image_data.image} alt='' />
              <p>Image: {latestImage.id}</p>
              <p>Defects: {latestImage.defects.length}</p>
              <p>Taken {moment(latestImage.create_time).calendar()}</p>
            </Fragment>
            :
            <p>Loading...</p>
          }
        </Card>
        <Card>
          {masksOverview ?
            <Plot
              data={[
                {
                  x: masksOverview.masks,
                  y: masksOverview.defects,
                  mode: 'scatter',
                },
              ]}
              config={{displayModeBar: false, scrollZoom: false}}
              layout={{
                width: 300,
                height: 300,
                title: 'Mask History',
                xaxis: {
                  title: "Mask ID",
                  range: [
                    masksOverview.masks[0] - .5,
                    masksOverview.masks[masksOverview.masks.length-1] + .5
                  ],
                  tick0: masksOverview.masks[0],
                  dtick: 1,
                  fixedrange: true,
                },
                yaxis: {
                  title: "Defects",
                  fixedrange: true,
                },
                showlegend: false,
                hovermode: 'closest',
              }}
            />
            :
            <p>Loading...</p>
          }
        </Card>
      </CardList>
    </div>
  )
}