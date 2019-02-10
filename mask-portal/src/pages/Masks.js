import React, { useState, useEffect } from 'react';

import api from 'js/api'
import Card from "components/CardList/Card"
import CardList from "components/CardList/CardList"

export default function Masks({ history }) {
  const [masks, setMasks] = useState();

  useEffect(
    () => {
      loadMasks();
    }
    , []
  )
  const loadMasks = async () => {
    const response = await api.get('/masks/');
    console.log(response.data);
    setMasks(response.data.results);
  }

  return (
    <div>
      {masks && masks.length > 0 && 
        <CardList>
          {masks.map(mask => 
            <Card key={mask.id} onClick={() => history.push(`/images/?mask=${mask.id}`)}>
              <p>Mask: {mask.id}</p>
              <p>Defect Positions: {mask.defect_position_count}</p>
              <p>Defect Images: {mask.defect_image_count}</p>
              <p>Defects: {mask.defect_count}</p>
            </Card>
          )}
        </CardList>
      }
      {masks && masks.length === 0 &&
        <p>No Masks Found</p>
      }
      {!masks &&
        <p>Loading...</p>
      }
    </div>
  )
}