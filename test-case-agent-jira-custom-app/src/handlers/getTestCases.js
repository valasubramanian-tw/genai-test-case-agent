import { fetch } from '@forge/api';

const getTestCases = async ({ payload: jira_issue }) => {
  console.log('Generating test cases for issueId:', jira_issue);
  const apiBaseUrl = 'https://rnjep-49-47-218-85.a.free.pinggy.link';
  const apiUrl = `${apiBaseUrl}/jira/tests`;
  const payload = JSON.stringify(jira_issue);
  console.log('Payload:', payload);
  const apiResponse = await fetch(apiUrl, {
    body: payload,
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Bypass-Tunnel-Reminder': 'test-case-agent',
      'X-Pinggy-No-Screen': 'true',
    }
  });
  
  const testCases = await apiResponse.json();
  console.log('Test cases generated:', testCases);
  return testCases?.response;
};

export default getTestCases;