import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown'
import './App.css'
import { events, invoke } from '@forge/bridge';

const App = () => {
  const [loading, setIsLoading] = useState(false);
  const [issue, setIssue] = useState(undefined);
  const [testCases, setTestCases] = useState(undefined);

  useEffect(() => {
    const fetchIssue = async () => {
      try {
        setIsLoading(true);
        const jiraIssue = await invoke('getJiraIssue');
        setIssue(jiraIssue);
      } catch (error) {
        console.error('Error fetching Jira issue:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchIssue();
    const subscribeForIssueChangedEvent = () =>
      events.on('JIRA_ISSUE_CHANGED', () => {
        fetchIssue();
      });
    const subscription = subscribeForIssueChangedEvent();

    return () => {
      subscription.then((subscription) => subscription.unsubscribe());
    };
  }, []);

  const handleGetTests = async () => {
    try {
        setIsLoading(true);
        console.log('Fetching test cases for issue:', issue);
        const testCases = await invoke('getTestCases', issue);
        setTestCases(testCases);
      } catch (error) {
        console.error('Error fetching Jira issue:', error);
      } finally {
        setIsLoading(false);
      }
  }

  const handleStreamTests = async () => {
    try {
      setIsLoading(true);
      setTestCases('');
      console.log('Generating test cases for issue:', issue);

      const chunks = await invoke('generateTestCases', issue);
      let fullResponse = '';

      for (const chunk of chunks) {
        if (chunk.type === 'message') {
          fullResponse += chunk.content;
          setTestCases(fullResponse);
        } else if (chunk.type === 'error') {
          console.error('Error from API:', chunk.content);
          break;
        }
      }
    } catch (error) {
      console.error('Error generating test cases:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStreamTests2 = async () => {
    try {
      setIsLoading(true);
      setTestCases(undefined);
      let fullResponse = '';
      console.log('generateTestCases:');
      const chunks = await invoke('generateTestCases', issue);
      
      for (const chunk of chunks) {
        if (chunk.type === 'message') {
          fullResponse += chunk.content;
          setTestCases(fullResponse);
        }
      }
    } catch (error) {
      console.error('Error generating test cases:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <>
      {!issue && (
        loading ?
        <div>
          <span>Loading Test Case Agent..</span>
        </div> :
        <div>
          <span>Error loading Test Case Agent. Try again later!</span>
        </div>
      )}
      {issue && (
        <div>
          <span>Hi there!</span>
          <br />
          <span>I'm your AI Assistant helps you to generate test cases for this story.</span>
          <br />
          <br />
          {loading && <span>Generating Test Cases...</span>}
          {(!loading && !testCases) && 
            <>
              <button appearance="primary" onClick={handleStreamTests}>Stream Test Cases</button>&nbsp;
              <button appearance="primary" onClick={handleGetTests}>Generate Test Cases</button>
            </>
          }
          {testCases && <ReactMarkdown children={testCases} />}
        </div>
      )}
    </>
  );
};

export default App;