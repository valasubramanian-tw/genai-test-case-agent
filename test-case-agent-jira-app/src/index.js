import Resolver from '@forge/resolver';
import api, { route } from '@forge/api';
import getJiraIssue from './handlers/getJiraIssue';
import streamTestCases from './handlers/streamTestCases';
import getTestCases from './handlers/getTestCases';
const resolver = new Resolver();

resolver.define('getJiraIssue', getJiraIssue);
resolver.define('streamTestCases', streamTestCases);
resolver.define('getTestCases', getTestCases);

export const handler = resolver.getDefinitions();
