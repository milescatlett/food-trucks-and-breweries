import React, { useEffect, useState } from "react";
import "./App.css";
import Container from 'react-bootstrap/Container'
import DataTable from './components/DataTable'

function App() {
  const [ftb, setData] = useState([]);

  useEffect(() => {
    (async () => {
      await fetch(
        "https://869c73fe39c7-3216997351929553973.ngrok-free.app/get-ftb", {
        method: 'GET', 
        mode: 'cors',
        headers: {
          'Access-Control-Allow-Origin':'*',
          "ngrok-skip-browser-warning": "69420"
        }
      }).then(response =>
        response.json().then(data => {
          setData(data.ftb);
        })
      );
    })();
  }, []);


  return (
    <Container style={{ marginTop: 40 }}>
        <DataTable ftb={ftb} />
    </Container>
  );
}

export default App;