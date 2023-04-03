import React from 'react';
import { ListGroup, Dropdown } from 'react-bootstrap';

// Mock data for testing
const currentUser = 'John Doe';
const models = ['Model 1', 'Model 2', 'Model 3'];
const threads = [
  { id: 1, title: 'Thread 1' },
  { id: 2, title: 'Thread 2' },
];
const publicThreads = [
  { id: 3, title: 'Public Thread 1' },
  { id: 4, title: 'Public Thread 2' },
];

const Sidebar = () => {
  const handleModelSelect = (selectedModel) => {
    console.log('Selected model:', selectedModel);
  };

  return (
    <div className="d-flex flex-column align-items-stretch bg-body-tertiary" style={{ width: '380px' }}>
      <div className="d-flex flex-column align-items-center p-3 bg-light">
        <h5>{currentUser}</h5>
        <Dropdown onSelect={handleModelSelect}>
          <Dropdown.Toggle variant="secondary" id="dropdown-basic">
            Select Model
          </Dropdown.Toggle>
          <Dropdown.Menu>
            {models.map((model, index) => (
              <Dropdown.Item key={index} eventKey={model}>
                {model}
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <a href="/" className="d-flex align-items-center p-3 link-body-emphasis text-decoration-none border-bottom">
        <span className="fs-5 fw-semibold">Threads</span>
      </a>
      <div className="list-group list-group-flush border-bottom scrollarea">
        {threads.map((thread) => (
          <a href="#" key={thread.id} className="list-group-item list-group-item-action py-3 lh-sm">
            <div className="d-flex w-100 align-items-center justify-content-between">
              <strong className="mb-1">{thread.title}</strong>
              <small>Model</small>
            </div>
            <div className="col-10 mb-1 small">
              {/* Add a description or other information related to the thread here. */}
            </div>
          </a>
        ))}
      </div>
      <a href="/" className="d-flex align-items-center p-3 link-body-emphasis text-decoration-none border-bottom">
        <span className="fs-5 fw-semibold">Public Threads</span>
      </a>
      <div className="list-group list-group-flush border-bottom scrollarea">
        {publicThreads.map((thread) => (
          <a href="#" key={thread.id} className="list-group-item list-group-item-action py-3 lh-sm">
            <div className="d-flex w-100 align-items-center justify-content-between">
              <strong className="mb-1">{thread.title}</strong>
              <small>Model</small>
            </div>
            <div className="col-10 mb-1 small">
              {/* Add a description or other information related to the public thread here. */}
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;