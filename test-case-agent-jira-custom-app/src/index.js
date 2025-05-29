import Resolver from '@forge/resolver';
import api, { route } from '@forge/api';
import getJiraIssue from './handlers/getJiraIssue';
import generateTestCases from './handlers/generateTestCases';
import getTestCases from './handlers/getTestCases';
const resolver = new Resolver();

resolver.define('getJiraIssue', getJiraIssue);
resolver.define('generateTestCases', generateTestCases);
resolver.define('getTestCases', getTestCases);

resolver.define('fetchLabels', async (req) => {
  const key = req.context.extension.issue.key;

  const res = await api.asUser().requestJira(route`/rest/api/3/issue/${key}?fields=labels`);

  const data = await res.json();

  const label = data.fields.labels;
  if (label == undefined) {
    console.warn(`${key}: Failed to find labels`);
    return [];
  }

  return label;
});

export const handler = resolver.getDefinitions();
