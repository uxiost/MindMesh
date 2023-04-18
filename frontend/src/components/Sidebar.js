import React, { useState, useEffect } from 'react';
import { ListGroup, Dropdown } from 'react-bootstrap';
import { Button, ButtonGroup } from 'react-bootstrap';
import { ResizableBox } from 'react-resizable';
import 'react-resizable/css/styles.css';
import { GoogleLogin, GoogleOAuthProvider } from '@react-oauth/google';
import axios from 'axios';

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

const clientId = process.env.REACT_APP_GOOGLE_CLIENT_ID;
const backendURL = process.env.REACT_APP_BACKEND_URL;

const Sidebar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userProfile, setUserProfile] = useState(null);
  const [llmIdentities, setLLMIdentities] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [selectedThreads, setSelectedThreads] = useState([]);
  const [publicThreads, setPublicThreads] = useState([]);

  const handleLoginSuccess = async (credentialResponse) => {
    const token = credentialResponse.credential;
    try {
      const response = await axios.post(`${backendURL}/authenticate`, {
        token,
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
  
      const userInfo = response.data;
      console.log('User info:', userInfo);
      setIsLoggedIn(true);
      setUserProfile(userInfo);
      
      // Store user profile data and idToken in local storage
      localStorage.setItem('userProfile', JSON.stringify(userInfo));
      localStorage.setItem('idToken', token);
    } catch (error) {
      console.error('Error during authentication:', error);
    }
  };
  
  useEffect(() => {
    const storedUserProfile = localStorage.getItem('userProfile');
    if (storedUserProfile) {
      setIsLoggedIn(true);
      setUserProfile(JSON.parse(storedUserProfile));
    }
  }, []);
  
  useEffect(() => {
    if (isLoggedIn) {
      const fetchData = async () => {
        try {
          const idToken = localStorage.getItem('idToken'); // Add this line to retrieve the idToken from local storage
          const response = await axios.get(`${backendURL}/llm-identities/user/${userProfile.google_account_id}`, {
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${idToken}`,
            },
          });
          setLLMIdentities(response.data);
        } catch (error) {
          console.error('Error fetching LLM identities:', error);
        }
      };
      fetchData();
    }
  }, [isLoggedIn, userProfile]);

  useEffect(() => {
    fetchPublicThreads();
  }, []);
  
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserProfile(null);
    localStorage.removeItem('userProfile');
    localStorage.removeItem('idToken');
  };

  const handleModelSelect = (selectedModel) => {
    console.log('Selected model:', selectedModel);
    setSelectedModel(selectedModel);
    fetchThreads(selectedModel);
  };
  
  const fetchThreads = async (modelName) => {
    try {
      const idToken = localStorage.getItem('idToken');
      const response = await axios.get(`${backendURL}/threads/model/${modelName}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`,
        },
      });
      setSelectedThreads(response.data);
    } catch (error) {
      console.error('Error fetching threads:', error);
    }
  };

  const fetchPublicThreads = async () => {
    try {
      const response = await axios.get(`${backendURL}/threads`);
      setPublicThreads(response.data);
    } catch (error) {
      console.error('Error fetching public threads:', error);
    }
  };
  

  return (
    <div className="d-flex flex-column align-items-stretch bg-body-tertiary" style={{ height: '100vh' }}>
  
  <div className="d-flex flex-column align-items-center p-3 bg-light">
        <h5>MindMesh</h5>
        {isLoggedIn ? (
  <div className="d-flex align-items-center">
    <p className="mb-0" style={{ marginRight: '8px' }}>Welcome, {userProfile.name}</p>
    <ButtonGroup size="sm">
      <Button variant="outline-secondary" onClick={handleLogout}>
        Logout
      </Button>
    </ButtonGroup>
  </div>
) : (
  <GoogleOAuthProvider clientId={clientId}>
    <GoogleLogin onSuccess={handleLoginSuccess} onError={error => console.log(error)} />
  </GoogleOAuthProvider>
)}


        {isLoggedIn ? (
          <Dropdown onSelect={handleModelSelect}>
            <Dropdown.Toggle variant="secondary" id="dropdown-basic">
              {selectedModel ? selectedModel : 'Select Model'}
            </Dropdown.Toggle>
            <Dropdown.Menu>
              {llmIdentities.map((identity, index) => (
                <Dropdown.Item key={index} eventKey={identity.model_name}>
                  {identity.model_name}
                </Dropdown.Item>
              ))}
            </Dropdown.Menu>
          </Dropdown>
        ) : (
          <p>Please log in to see your LLM identities.</p>
        )}


      </div>
      <ResizableBox width={Infinity} height={500} axis="y" minConstraints={[Infinity, 50]} maxConstraints={[Infinity, 1000]}>
        <div className="d-flex flex-column">
          <a href="/" className="d-flex align-items-center p-3 link-body-emphasis text-decoration-none border-bottom">
            <span className="fs-5 fw-semibold">Threads</span>
          </a>
          <div className="list-group list-group-flush border-bottom scrollarea">
            {selectedThreads.map((thread) => (
              <a href="#" key={thread.id} className="list-group-item list-group-item-action py-3 lh-sm">
                <div className="d-flex w-100 align-items-center justify-content-between">
                  <strong className="mb-1">{thread.title}</strong>
                  <small>{selectedModel}</small>
                </div>
                <div className="col-10 mb-1 small">
                  {/* Add a description or other information related to the thread here. */}
                </div>
              </a>
            ))}
          </div>
        </div>
      </ResizableBox>
      <div className="d-flex flex-column">
        <a href="/" className="d-flex align-items-center p-3 link-body-emphasis text-decoration-none border-bottom">
          <span className="fs-5 fw-semibold">Public Threads</span>
        </a>
        <div className="list-group list-group-flush border-bottom scrollarea">
          {publicThreads.map((thread) => (
            <a href="#" key={thread.id} className="list-group-item list-group-item action py-3 lh-sm">
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
    </div>
  );
};
            
export default Sidebar;
