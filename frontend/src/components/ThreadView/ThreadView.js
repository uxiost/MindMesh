import React from 'react';
import { Card } from 'react-bootstrap';
import Conversation from './Conversation';

const ThreadView = ({ thread }) => {
  if (!thread) {
    return <div>Please select a thread to view the conversation.</div>;
  }

  return (
    <Card>
      <Card.Header>
        <h5>{thread.title}</h5>
        <p className="mb-0">Visibility: {thread.isPrivate ? 'Private' : 'Public'}</p>
      </Card.Header>
      <Card.Body>
        <Conversation messages={thread.messages} />
      </Card.Body>
    </Card>
  );
};

export default ThreadView;
