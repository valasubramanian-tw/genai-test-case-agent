import { eventEmitter, EVENT_TYPES } from './eventEmitter';

const apiStreamTestCases = async ({ jira_issue, format, limit }) => {
  console.log('Generating test cases for:', jira_issue);
  const apiBaseUrl = 'http://localhost:8000'
  const apiUrl = `${apiBaseUrl}/stream/jira/tests`;
  const payload = JSON.stringify({
    story: jira_issue,
    format: format,
    limit: limit
  });
  
  try {
    const response = await fetch(apiUrl, {
      body: payload,
      method: 'POST',
      headers: {
        'Accept': 'text/event-stream',
        'Content-Type': 'application/json',
        'Bypass-Tunnel-Reminder': 'test-case-agent',
        'X-Pinggy-No-Screen': 'true',
      }
    });

    const text = await response.text();
    const lines = text.split('\n').filter(line => line.trim());

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        try {
          const data = JSON.parse(line.slice(6));
          // console.log('Handler: Emitting test case chunk:', data);
          eventEmitter.emit(EVENT_TYPES.TEST_CASE_CHUNK, data);
        } catch (error) {
          console.error('Handler: Error parsing SSE data:', error);
          eventEmitter.emit(EVENT_TYPES.TEST_CASE_ERROR, error.message);
        }
      }
    }
    
    eventEmitter.emit(EVENT_TYPES.TEST_CASE_COMPLETE);
    return { status: 'streaming_started' };
  } catch (error) {
    eventEmitter.emit(EVENT_TYPES.TEST_CASE_ERROR, error.message);
    throw error;
  }
};

export default apiStreamTestCases;