import Resolver from '@forge/resolver';
import api, { route, fetch } from '@forge/api'; 

const resolver = new Resolver();

resolver.define('getText', (req) => {
  console.log(req);
  return 'Hello, world!';
});

resolver.define('getLocalComments', async () => {
  console.log('Fetching local comments');
  //http://localhost:55372/jira/comments
  //https://bc74-157-51-77-78.ngrok-free.app
  const localComments = await fetch('https://bf6ef6c8abc28e450e888d6c6b6bbe63.serveo.net/jira/comments', {
    headers: {
      'Accept': 'application/json'
    }
  });
  const responseData = await localComments.json();
  console.log('Local comments fetched:', responseData);
  return responseData;
});

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
