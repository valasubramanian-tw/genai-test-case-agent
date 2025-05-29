import api, { route } from '@forge/api'; 

const getJiraIssue = async ({ context }) => {
    const issueId = context.extension.issue.key;
    console.log('Fetching details for issueId:', issueId);
    const apiResponse = await api.asApp().requestJira(route`/rest/api/2/issue/${issueId}`, {
        headers: {
            'Accept': 'application/json'
        }
    });
    const issueDetails = await apiResponse.json();
    const jiraStory = {
        key: issueDetails.key,
        summary: issueDetails.fields.summary,
        description: issueDetails.fields.description || '',
        status: issueDetails.fields.status.name
    };
    return jiraStory;
}

export default getJiraIssue;