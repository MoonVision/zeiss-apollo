import React, { useState, useEffect } from 'react';
import moment from 'moment';

import api from 'js/api'
import Card from "components/CardList/Card"
import CardList from "components/CardList/CardList"

export default function Images({ match, history, location }) {
  let params = new URLSearchParams(location.search);
  const [images, setImages] = useState();
  const selectedMask = params.get('mask')
  const [currentMask, setCurrentMask] = useState(selectedMask);

  useEffect(
    () => {
      loadImages();
    }
    , [selectedMask]
  )
  const loadImages = async () => {
    const response = await api.get('/defectpositionimages/', {params: {mask: selectedMask}});
    setImages(response.data.results);
  }

  return (
    <div>
      <label>Mask ID:</label>
      <input type='text'
              value={currentMask}
              onChange={e => setCurrentMask(e.target.value)}
      />
      <button
        disabled={selectedMask===currentMask}
        onClick={() => {
          params.set('mask', currentMask);
          history.push({location, search: params.toString() });
        }}
      >
        Update
      </button>
      <button
        disabled={selectedMask===null}
        onClick={() => {
          params.delete('mask');
          history.push({location, search: params.toString() });
        }}
      >
        Clear
      </button>
      {images && images.length > 0 && 
        <CardList>
          {images.map(image => 
            <Card key={image.id}>
              <img src={image.image.image} alt='' />
              <p>Image: {image.id}</p>
              <p>Defects: {image.defects.length}</p>
              <p>Taken {moment(image.create_time).calendar()}</p>
            </Card>
          )}
        </CardList>
      }
      {images && images.length === 0 &&
        <p>No Images Found</p>
      }
      {!images &&
        <p>Loading...</p>
      }
    </div>
  )
}