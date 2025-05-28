import { fetch, route } from '@forge/api';

const generateTestCases = async ({ context, onChunk }) => {
  const issueId = context.extension.issue.key;
  console.log('Generating test cases for issueId:', issueId);
  
  const apiBaseUrl = 'https://0a02034d906b6a4b086040a9ace7a090.serveo.net';
  const apiUrl = `${apiBaseUrl}/stream/jira/${issueId}/tests`;
  
  const response = await fetch(apiUrl, {
    headers: {
      'Accept': 'text/event-stream'
    }
  });

  const text = await response.text();
  const lines = text.split('\n');
  let buffer = '';

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      try {
        const data = JSON.parse(line.slice(6));
        if (onChunk && typeof onChunk === 'function') {
          onChunk(data);
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
      }
    }
  }

  return true;
};

export default generateTestCases;