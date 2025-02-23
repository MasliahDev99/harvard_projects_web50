# Network Project

This project is a social networking platform where users can create posts, follow other users, and interact with posts through likes and comments.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **Create Posts**: Authenticated users can create new posts.
- **Profile Pages**: Users have profile pages displaying their posts and follower statistics.
- **Follow System**: Users can follow and unfollow other users.
- **Pagination**: Posts are paginated for better user experience.

## Specification

1. **New Post**:
   - Users who are signed in should be able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

2. **All Posts**:
   - The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, with the most recent posts first.

3. **Profile Page**:
   - Clicking on a username should load that user’s profile page, displaying the number of followers and followings, and all posts by the user in reverse chronological order.

4. **Following**:
   - The “Following” link in the navigation bar should take the user to a page where they see all posts made by users that the current user follows.

5. **Pagination**:
   - On any page that displays posts, posts should only be displayed 10 on a page. Implement “Next” and “Previous” buttons for navigation.

6. **Edit Post**:
   - Users should be able to click an “Edit” button on any of their own posts to edit that post, with changes saved without a page reload.

7. **Like and Unlike**:
   - Users should be able to click a button on any post to toggle whether or not they “like” that post, with the like count updated asynchronously.



## Challenges

- **Like/Unlike System**: The current challenge is implementing the like and unlike system to update the UI correctly. This involves ensuring the server correctly processes like toggles and the client-side JavaScript updates the like count and button state without a page reload.

- **Pagination**: Implementing pagination to ensure that posts are displayed in a user-friendly manner, with navigation controls for "Next" and "Previous" pages, was a significant challenge. This required careful handling of page numbers and ensuring that the correct posts are displayed on each page.

- **Reusable Components**: Creating reusable components like `posts.html` and `paginator.html` was another challenge. These components needed to be flexible enough to be used across different parts of the application, requiring thoughtful design and parameterization to ensure they could adapt to various contexts.


## Demo

[![YouTube Video Thumbnail](https://img.youtube.com/vi/HhigHEpRczs/0.jpg)](https://youtu.be/HhigHEpRczs)


## Getting Started

To get started with the project, clone the repository and set up the environment as follows:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

