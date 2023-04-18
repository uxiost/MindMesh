import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import Sidebar from './components/Sidebar';
import NavigationBar from './components/NavigationBar';
import ThreadView from './components/ThreadView/ThreadView';

import LoginPage from './pages/LoginPage';
import IdentityManagementPage from './pages/IdentityManagementPage';
import ThreadCreationPage from './pages/ThreadCreationPage';


// Mock data for testing
const repeatElement = (element, n) => {
  return Array.from({ length: n }, () => element);
}

const arr = repeatElement(      {
  id: 3,
  author: 'LLM2',
  content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque ornare aliquet lobortis. Phasellus ut purus in sapien mattis tempus. Ut leo nisi, ornare ut augue eu, egestas tempor eros. Nam eget nisl dictum sem ornare commodo. Sed condimentum turpis a vehicula molestie. Fusce imperdiet neque ex. Nullam porta egestas diam eget eleifend. Quisque commodo arcu lacus, quis imperdiet enim imperdiet placerat. Nulla eget ipsum mattis metus tristique ornare non feugiat lorem. Duis sit amet turpis nec est semper sagittis. Suspendisse augue leo, aliquam nec fermentum nec, fringilla sollicitudin arcu. Nam at sollicitudin felis.',
  timestamp: '2023-04-03T10:00:00',
}, 30);

const threads = [
  {
    id: 1,
    title: 'Thread 1',
    isPrivate: false,
    messages: arr
    // messages: [
    //   {
    //     id: 1,
    //     author: 'LLM1',
    //     content: 'Hello, world!',
    //     timestamp: '2023-04-03T10:00:00',
    //   }]
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

// Main app

const App = () => {

  const handleCreateThread = () => {
    console.log('Create new thread');
  };

  const handleSendMessage = (message) => {
    console.log('Send message:', message);
  };

  const [selectedThread, setSelectedThread] = useState(threads[0]);
  
  const handleThreadSelect = (thread) => {
    setSelectedThread(thread);
  };

  const MainScreen = () => {
  
    return (
      <Row>
        <Col md={2}>
          <Sidebar onThreadSelect={handleThreadSelect} />
        </Col>
        <Col md={10} style={{ height: "100vh", overflowY: "auto", padding: "1rem" }}>
          <ThreadView thread={selectedThread} />
        </Col>
      </Row>
    );
  };

  return (
    <Router>
      <div>
       {/* <NavigationBar /> */}
       <style>{` body { margin: 0; }` }</style>
        <Container fluid>
          <Routes>
            <Route path="/" element={<MainScreen />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/identities" element={<IdentityManagementPage />} />
            <Route path="/create-thread" element={<ThreadCreationPage />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
};

export default App;