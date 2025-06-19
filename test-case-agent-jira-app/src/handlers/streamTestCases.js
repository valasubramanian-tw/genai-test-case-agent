import { fetch } from '@forge/api';
import { eventEmitter, EVENT_TYPES } from '../../static/ui/src/services/eventEmitter';

const streamTestCases = async ({ payload: jira_issue }) => {
  console.log('Generating test cases for:', jira_issue);
  const apiBaseUrl = 'https://bcef682f3e54e4526b8fea1e8fed2fff.serveo.net';
  const apiUrl = `${apiBaseUrl}/stream/jira/tests`;
  const apiPayload = JSON.stringify(jira_issue);
  
  try {
    const response = await fetch(apiUrl, {
      body: apiPayload,
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

export default streamTestCases;