import React from 'react';
import { ListGroup } from 'react-bootstrap';

const Conversation = ({ messages }) => {
  return (
    <ListGroup>
      {messages.map((message, index) => (
        <ListGroup.Item key={index} className="border-0">
          <div className="d-flex w-100 align-items-start">
            <strong className="me-2">{message.author}:</strong>
            <div className="text-wrap">
              <p className="mb-0">{message.content}</p>
              <small className="text-muted">{message.timestamp}</small>
            </div>
          </div>
        </ListGroup.Item>
      ))}
    </ListGroup>
  );
};

export default Conversation;
