import React from 'react';
import Button from 'react-bootstrap/Button';
import Navbar from 'react-bootstrap/Navbar';
import Card from 'react-bootstrap/Card';

function App() {
  return (
    <div className="app">

      <div className="ava-container-nav">
            <h2 class="text-center">CRISPR Analyzer</h2>
      </div>

      <div className="ava-left-container">
        <div className="ava-card-container">
          <Card style={{ height:'100%' }}>

            <Card.Header>
              <Card.Title>Options</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">Select the model and data for analysis.</Card.Subtitle>
            </Card.Header>

            <Card.Body>
              <Card.Text>

                <p className="ava-bold"> Model: </p>
                Some quick example text to build on the card title and make up the bulk of
                the card's content.
          
                <p className="ava-bold"> Data: </p>
                Some quick example text to build on the card title and make up the bulk of
                the card's content.
              </Card.Text>

              <Card.Link style={{ bottom:'0px' }} href="#">
                <Button variant="primary">Run</Button>{' '}
              </Card.Link>

            </Card.Body>
          </Card>
        </div>
      </div>

      <div className="ava-right-container">
      <Card className="text-center" style={{ height:'100%' }}>
        <Card.Body>

          <div className="ava-text-container">
            <div className="ava-block">
              <svg width="2em" height="1em" viewBox="0 0 16 16" class="bi bi-bar-chart" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" d="M4 11H2v3h2v-3zm5-4H7v7h2V7zm5-5h-2v12h2V2zm-2-1a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1h-2zM6 7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm-5 4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3z"/>
              </svg>

              <Card.Text>
                The plot will appear here, once you have selected options.
              </Card.Text>
            </div>
          </div>

        </Card.Body>
      </Card>
      </div>
    </div>
  );
}

export default App;
