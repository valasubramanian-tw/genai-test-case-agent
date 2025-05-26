import React, { useEffect, useState } from 'react';
import { Box, Button, Text, useProductContext } from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const context = useProductContext();
  const [issue, setIssue] = useState();
  const [testCases, setTestCases] = useState(undefined);
  const [loading, setIsLoading] = useState(false);

  const generateTestCases = async () => {
    console.log('Initializing fetch generateTestCases');
    setIsLoading(true);
    const testCases = await invoke('generateTestCases');
    setTestCases(testCases);
    setIsLoading(false);
  }
  
  console.log('Context:', context);
  return (
    <>
      <Box padding="medium">
        <Text>Hi there!</Text>
        <Text>I'm your AI Assistant helps you to generate test cases for this story.</Text>
        {loading && <Text>Generating Test Cases...</Text>}
        {(!loading && !testCases) && 
          <Button appearance="primary" onClick={generateTestCases}>Generate Test Cases</Button>}
      </Box>
      {testCases &&
        <Box>
          <Text>Test Cases:</Text>
          {testCases && <Text>{testCases}</Text>}
        </Box>
      }
    </>
  );
};

export default App;