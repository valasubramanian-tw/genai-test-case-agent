import Resolver from '@forge/resolver';
import getJiraIssue from './handlers/getJiraIssue';
import generateTestCases from './handlers/generateTestCases';
import getTestCases from './handlers/getTestCases';

const resolver = new Resolver();

resolver.define('getJiraIssue', getJiraIssue);
resolver.define('generateTestCases', generateTestCases);
resolver.define('getTestCases', getTestCases);

export const handler = resolver.getDefinitions();
