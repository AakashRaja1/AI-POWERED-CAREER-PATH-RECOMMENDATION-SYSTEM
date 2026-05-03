/*
About page. It explains the project idea, purpose, and major features in user-facing language.

Presentation note: this comment is here to help explain the file quickly during viva or panel questions without changing runtime behavior.
*/

import React from 'react';

const About = () => {
  return (
    <div className="container mx-auto p-4 bg-white text-gray-900 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">About Us</h1>
      <p>This project is an AI-Powered Career Path Recommendation System. Our goal is to help individuals find their ideal career path based on their skills, interests, and experience.</p>
    </div>
  );
};

export default About;
