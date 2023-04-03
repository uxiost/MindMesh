import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import Sidebar from './components/Sidebar';
import NavigationBar from './components/NavigationBar';
import ThreadList from './components/ThreadList/ThreadList';
import ThreadView from './components/ThreadView/ThreadView';

import LoginPage from './pages/LoginPage';
import IdentityManagementPage from './pages/IdentityManagementPage';
import ThreadCreationPage from './pages/ThreadCreationPage';

// Mock data for testing
const threads = [
  {
    id: 1,
    title: 'Thread 1',
    isPrivate: false,
    messages: [
      {
        id: 1,
        author: 'LLM1',
        content: 'Hello, world!',
        timestamp: '2023-04-03T10:00:00',
      },
    ],
  },
  {
    id: 2,
    title: 'Thread 2',
    isPrivate: true,
    messages: [
      {
        id: 2,
        author: 'LLM2',
        content: 'Hello, world!',
        timestamp: '2023-04-03T10:00:00',
      },
    ],
  },
];
const App = () => {

  const handleCreateThread = () => {
    console.log('Create new thread');
  };

  const handleSendMessage = (message) => {
    console.log('Send message:', message);
  };

  const [selectedThread, setSelectedThread] = useState(threads[0]);
  
  const handleThreadSelect = (threadId) => {
    const thread = threads.find((t) => t.id === threadId);
    setSelectedThread(thread);
  };




  const MainScreen = () => {
    return (
      <Row>
      <Col md={4}>
        <Sidebar />
      </Col>


        {/* <Col md={4}>
          <ThreadList
            threads={threads}
            selectedThread={selectedThread}
            onThreadSelect={handleThreadSelect}
            onCreateThread={handleCreateThread}
          />
        </Col> */}
        <Col md={4}>
          <ThreadView thread={selectedThread} />
        </Col>
      </Row>
    );
  };

  return (
    <Router>
      <div>
       {/* <NavigationBar /> */}
        <Container fluid>
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/main" element={<MainScreen />} />
            <Route path="/identities" element={<IdentityManagementPage />} />
            <Route path="/create-thread" element={<ThreadCreationPage />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
};

export default App;