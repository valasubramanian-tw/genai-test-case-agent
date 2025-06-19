const apiGetTestCases = async ({ jira_issue, format, limit }) => {
  console.log('Generating test cases for issueId:', jira_issue);
  const apiBaseUrl = 'http://localhost:8000'
  const apiUrl = `${apiBaseUrl}/jira/tests`;
  const payload = JSON.stringify({
    story: jira_issue,
    format: format,
    limit: limit
  });
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

export default apiGetTestCases;