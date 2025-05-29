import { fetch } from '@forge/api';

const generateTestCases = async ({ payload: jira_issue }) => {
  console.log('Generating test cases for:', jira_issue);
  const apiBaseUrl = 'https://rnjep-49-47-218-85.a.free.pinggy.link';
  const apiUrl = `${apiBaseUrl}/stream/jira/tests`;
  const apiPayload = JSON.stringify(jira_issue);
  console.log('Payload:', apiPayload);
  const apiResponse = await fetch(apiUrl, {
    body: apiPayload,
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Bypass-Tunnel-Reminder': 'test-case-agent',
      'X-Pinggy-No-Screen': 'true',
    }
  });

  const text = await apiResponse.text();
  const lines = text.split('\n');
  const chunks = [];

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      try {
        const data = JSON.parse(line.slice(6));
        chunks.push(data);
      } catch (error) {
        console.error('Error parsing SSE data:', error);
      }
    }
  }

  return chunks;
};

export default generateTestCases;