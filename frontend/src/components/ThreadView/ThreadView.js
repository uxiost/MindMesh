import React from 'react';
import { Card } from 'react-bootstrap';
import Conversation from './Conversation';

const ThreadView = ({ thread }) => {
  if (!thread) {
    return <div>Please select a thread to view the conversation.</div>;
  }

  return (
    <div style={{ width: '100%', height: '100%', maxHeight: '100%', overflowY: 'auto', padding: '1rem', boxSizing: 'border-box', border: '1px solid #dee2e6', borderRadius: '0.25rem' }}>
      <h5>{thread.title}</h5>
      <p className="mb-0">Visibility: {thread.isPrivate ? 'Private' : 'Public'}</p>
      <hr />
      <Conversation messages={thread.messages} />
    </div>
  );
};

export default ThreadView;
