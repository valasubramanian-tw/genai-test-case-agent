import { fetch } from '@forge/api';

const getTestCases = async ({ payload: jira_issue }) => {
  console.log('Generating test cases for issueId:', jira_issue);
  const apiBaseUrl = 'https://cba60fbb87253d60fca29ae7a52de0c8.serveo.net';
  const apiUrl = `${apiBaseUrl}/jira/tests`;
  const payload = JSON.stringify(jira_issue);
  const apiResponse = await fetch(apiUrl, {
    body: payload,
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  });
  
  const testCases = await apiResponse.json();
  console.log('Test cases generated:', testCases);
  return testCases?.response;
};

export default getTestCases;