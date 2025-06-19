import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown'
import { AnimatedMarkdown } from 'flowtoken';
import './App.css'
import { events, invoke } from '@forge/bridge';
import { eventEmitter, EVENT_TYPES } from './services/eventEmitter';
import apiGetTestCases from './services/apiGetTestCases';
import apiStreamTestCases from './services/apiStreamTestCases';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';

const App = () => {
  const [loading, setIsLoading] = useState(false);
  const [format, setFormat] = useState('JSON'); // Default format
  const [limit, setLimit] = useState(10); // Default limit
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

  useEffect(() => {
    const handleTestCaseChunk = (event) => {
      const { detail } = event;
      if (detail.type === 'message') {
        setTestCases(prev => (prev || '') + detail.content);
        console.log('handleTestCaseChunk data', detail.content);
      }
    };

    const handleTestCaseError = (event) => {
      console.error('handleTestCaseError Error generating test cases:', event.detail);
      setIsLoading(false);
    };

    const handleTestCaseComplete = () => {
      console.log('handleTestCaseComplete');
      setIsLoading(false);
    };

    // Add event listeners
    eventEmitter.addEventListener(EVENT_TYPES.TEST_CASE_CHUNK, handleTestCaseChunk);
    eventEmitter.addEventListener(EVENT_TYPES.TEST_CASE_ERROR, handleTestCaseError);
    eventEmitter.addEventListener(EVENT_TYPES.TEST_CASE_COMPLETE, handleTestCaseComplete);

    // Cleanup function
    return () => {
      eventEmitter.removeEventListener(EVENT_TYPES.TEST_CASE_CHUNK, handleTestCaseChunk);
      eventEmitter.removeEventListener(EVENT_TYPES.TEST_CASE_ERROR, handleTestCaseError);
      eventEmitter.removeEventListener(EVENT_TYPES.TEST_CASE_COMPLETE, handleTestCaseComplete);
    };
  }, []);

  const handleFormatChange = (event) => {
    setFormat(event.target.value);
  };

  const handleLimitChange = (event) => {
    setLimit(Number(event.target.value));
  };

  const handleGetTests = async () => {
    try {
        setIsLoading(true);
        console.log('Fetching test cases for issue:', issue);
        // const testCases = await invoke('getTestCases', issue);
        const testCases = await apiGetTestCases({ jira_issue: issue, format: format, limit: limit });
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
      console.log('Streaming test cases for issue:', issue);
      // await invoke('streamTestCases', issue);
      await apiStreamTestCases({ jira_issue: issue, format: format, limit: limit });
    } catch (error) {
      console.error('Error generating test cases:', error);
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
          <span>From Stories to Test Cases – Automatically generate test cases from your user stories.</span>
          <br />
          <span>Transform acceptance criteria into actionable test cases in one click.</span>
          <br />
          <br />
          {!loading && 
            <Grid container spacing={1}>
              <Grid size={2}>
                <FormControl fullWidth size="small">
                  <InputLabel id="demo-simple-select-format">Format:</InputLabel>
                  <Select
                    labelId="demo-simple-select-format"
                    id="demo-simple-select-format"
                    value={format}
                    label="Output Format"
                    onChange={handleFormatChange}
                  >
                    <MenuItem value="Markdown">Markdown</MenuItem>
                    {/* <MenuItem value="Table">Table</MenuItem> */}
                    <MenuItem value="JSON">JSON</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={2}>
                <FormControl fullWidth size="small">
                  <InputLabel id="demo-simple-select-limit">Number of Test Cases:</InputLabel>
                  <Select
                    labelId="demo-simple-select-limit"
                    id="demo-simple-select-limit"
                    value={limit}
                    label="Number of Test Cases"
                    onChange={handleLimitChange}
                  >
                    <MenuItem value="5">5</MenuItem>
                    <MenuItem value="10">10</MenuItem>
                    <MenuItem value="15">15</MenuItem>
                    <MenuItem value="20">20</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid size={4}>
                <FormControl fullWidth size="small">
                  <TextField fullWidth size="small" label="Custom Instructions (optional)" />
                </FormControl>
              </Grid>
              <Grid size={4}>
                <Button variant="contained" size="small" onClick={handleStreamTests}>Generate Test Cases</Button>&nbsp;
                {/* <Button variant="contained" size="small" onClick={handleGetTests}>Generate Test Cases</Button> */}
              </Grid>
            </Grid>
          }
          {loading && 
            <Box sx={{ width: '100%' }}>
              <span>Generating Test Cases...</span>
              <br />
              <br />
              <LinearProgress />
            </Box>
          }
          {!loading && testCases && 
            <>
              <br />
              <br />
              <Grid container spacing={2}>
                <ReactMarkdown children={testCases} />
                {/* <AnimatedMarkdown
                  content={testCases}
                  animation="fadeIn"
                  animationDuration="0.5s"
                  animationTimingFunction="ease-in-out"
                /> */}
              </Grid>
              <br />
              <br />
              <Grid container spacing={2}>
                <Grid size={8}>
                  <FormControl fullWidth size="small">
                    <TextField fullWidth size="small" label="Ask a question or any specfic test cases to generate" />
                  </FormControl>
                </Grid>
                <Grid size={4}>
                  <Button variant="outlined" size="small">Ask</Button>&nbsp;
                </Grid>
              </Grid>
              <br />
            </>
          }
        </div>
      )}
    </>
  );
};

export default App;