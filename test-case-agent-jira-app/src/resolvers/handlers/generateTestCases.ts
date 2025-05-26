import { fetch } from '@forge/api';

const generateTestCases  = async ({ context }) => {
  console.log('Generating test cases...');
  const apiUrl = 'https://2334e981445f3a85a7729b72a291252f.serveo.net/generate/tests/jira/123123';
  const apiResponse = await fetch(apiUrl, {
    headers: {
      'Accept': 'application/json'
    }
  });
  const testCases = await apiResponse.json();
  console.log('Test cases generated:', testCases);
  return testCases?.response;
};

export default generateTestCases;
