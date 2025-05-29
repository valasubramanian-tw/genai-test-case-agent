import React, { useEffect, useState } from 'react';
import { Box, Button, SectionMessage, Text, useProductContext } from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const context = useProductContext();
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
  }
  , [context]);

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
      setTestCases(undefined);
      let fullResponse = '';

      await invoke('generateTestCases', { context: context })({
        onChunk: (data) => {
          if (data.type === 'message') {
            fullResponse += data.content;
            setTestCases(fullResponse);
          }
        }
      });
    } catch (error) {
      console.error('Error generating test cases:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  console.log('Context:', context);
  return (
    <>
      {!issue && (
        loading ?
        <Box padding="medium">
          <Text>Loading Test Case Agent..</Text>
        </Box> :
        <Box padding="medium">
          <Text>Error loading Test Case Agent. Try again later!</Text>
        </Box>
      )}
      {issue && (
        <Box padding="medium">
          <Text>Hi there!</Text>
          <Text>I'm your AI Assistant helps you to generate test cases for this story.</Text>
          {loading && <Text>Generating Test Cases...</Text>}
          {(!loading && !testCases) && 
            <Button appearance="primary" onClick={handleGetTests}>Generate Test Cases</Button>}
          {testCases &&
            <Box>
              <SectionMessage title="Test Cases" appearance='discovery'>{testCases}</SectionMessage>
            </Box>
          }
        </Box>
      )}
    </>
  );
};

export default App;