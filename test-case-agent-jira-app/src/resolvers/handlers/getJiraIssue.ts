import api, { route } from '@forge/api'; 

const getJiraIssue = async ({ context }) => {
    const issueId = context.extension.issue.key;
    console.log('Fetching details for issueId:', issueId);
    const apiResponse = await api.asApp().requestJira(route`/rest/api/3/issue/${issueId}`, {
        headers: {
            'Accept': 'application/json'
        }
    });
    const issueDetails = await apiResponse.json();
    return issueDetails;
}

export default getJiraIssue;