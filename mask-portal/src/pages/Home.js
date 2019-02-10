import React, { useState, useEffect } from 'react';
import moment from 'moment';

import Card from "components/CardList/Card"
import CardList from "components/CardList/CardList"

export default function Home() {
  const [latestImage, setLatestImage] = useState();

  const [masksOverview, setMasksOverivew] = useState();
  return (
    <div>
      <CardList>
        <Card>
          <h3>Latest Image</h3>
          <img src={latestImage.image_data.image} alt='' />
          <p>Image: {latestImage.id}</p>
          <p>Defects: {latestImage.defects.length}</p>
          <p>Taken {moment(latestImage.create_time).calendar()}</p>
        </Card>

      </CardList>
    </div>
  )
}