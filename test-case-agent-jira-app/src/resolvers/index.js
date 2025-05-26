import Resolver from '@forge/resolver';
import api, { route, fetch } from '@forge/api';
import getJiraIssue from './handlers/getJiraIssue';
import generateTestCases from './handlers/generateTestCases';

const resolver = new Resolver();

resolver.define('getText', (req) => {
  console.log(req);
  return 'Hello, world!';
});

resolver.define('getJiraIssue', getJiraIssue);
resolver.define('generateTestCases', generateTestCases);

resolver.define('getComments', async ({context}) => {
  const issueId = context.extension.issue.key;
  console.log('Fetching comments for issue:', issueId);
  // API call to get all comments of Jira issue with key
  const commentsData = await api.asApp().requestJira(route`/rest/api/3/issue/${issueId}/comment`, {
    headers: {
      'Accept': 'application/json'
    }
  });

  // API call to get all comments of Jira issue with key
  const responseData = await commentsData.json();
  const jsonData = await responseData.comments

  let extractedTexts = [];

  // Extracting all texts in the comments into extractedTexts array
  await jsonData.map(comment => {
    if (comment.body && comment.body.content) {
      comment.body.content.map(contentItem => {
        if (contentItem.type === "paragraph" && contentItem.content) {
          contentItem.content.map(textItem => {
            if (textItem.type === "text" && textItem.text) {
              extractedTexts.push(textItem.text);
            }
          });
        }
      });
    }
  });

  return extractedTexts.join(' ');
});

export const handler = resolver.getDefinitions();
