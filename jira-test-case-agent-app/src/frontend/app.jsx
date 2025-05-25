import React, { useEffect, useState } from 'react';
import { Text, useProductContext } from '@forge/react';
import { invoke } from '@forge/bridge';

const App = () => {
  const context = useProductContext();
  const [comments, setComments] = useState();

  useEffect(() => {
    const getCommentSummary = async () => {
      console.log('Initializing fetch comments');
      const commentsData = await invoke('getLocalComments');
      console.log("Comments - " + commentsData);
      setComments(commentsData);
    };
    getCommentSummary();
  }, []);
  
  console.log('Context:', context);
  return (
    <>
      <Text>Hello Vala!!</Text>
      <Text>Number of comments on this issue: {comments?.length}</Text>
    </>
  );
};

export default App;