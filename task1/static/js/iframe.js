import Iframe from 'react-iframe';
import React, { Component } from "react";

class TableList extends React.Component {
    render() {
    return(
      <div><
        <Iframe url="https://eyeshu98.grafana.net/d/Wmsy-HRGz/query?orgId=1"
          width="100%"
          height="1000"
          id="myId"
          // className="embed-responsive-item"
          display="initial"
          position="relative"
          X-Frame-Options="deny"
        />
     </div>
   )
  }
}
export default TableList;
