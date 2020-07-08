import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Navbar from 'react-bootstrap/Navbar';
import Card from 'react-bootstrap/Card';

var tools = require('./tools.json');


function App() {

  const [selectedTool, setSelectedTool] = useState({});
  const [hasSelectedTool, setHasSelectedTool] = useState(false);

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


                <div class="form-group row">
                  <label><p className="ava-bold"> Model: </p> </label>
                  <div className="ava-select-cont">
                    <select class="form-control form-control-sm"  onChange={(e) => {setSelectedTool(tools[e.target.value]); setHasSelectedTool(true)}}>
                      <option value={-1}>Please select a model...</option>
                      {
                        tools.map((tool,index) => <option value={index}>{tool.name}</option>)
                      }
                    </select>
                  </div>
                </div>

                <p className="ava-description">

                {(hasSelectedTool) ? <div><p className="ava-descript-header">Description:</p> {selectedTool.description} </div> : <div></div>}
                {(hasSelectedTool) ? <div><p className="ava-descript-header">Source:</p> <a href={selectedTool.link}>{selectedTool.link}</a> </div> : <div></div>}
                </p>

                <div class="form-group row">
                  <label><p className="ava-bold"> Dataset: </p> </label>
                  <div className="ava-select-cont">
                    <select class="form-control form-control-sm">
                      <option>Xu</option>
                      <option>Doench</option>
                    </select>
                  </div>
                </div>

                <p className="ava-description">
                Some quick example text to build on the card title and make up the bulk of
                the card's content.
                </p>


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
