import React from 'react';
import { Card, Button, ListGroup } from 'react-bootstrap';

const ThreadList = ({ threads, onCreateThread }) => {
  return (
    <Card className="mb-3">
      <Card.Header className="bg-primary text-white">
        Threads
      </Card.Header>
      <ListGroup variant="flush">
        {threads.map((thread) => (
          <ListGroup.Item key={thread.id} className="text-truncate">
            {thread.title}
          </ListGroup.Item>
        ))}
      </ListGroup>
      <Card.Footer className="text-center">
        <Button onClick={onCreateThread} variant="secondary">
          Create Thread
        </Button>
      </Card.Footer>
    </Card>
  );
};

export default ThreadList;