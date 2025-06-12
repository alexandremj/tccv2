// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Chain {
    struct Post {
        uint128 id;
        string creatorId;
        string content;
        bool active;
    }
    event PostCreated(uint256 indexed postId);

    Post[] public posts;

    function createPost(string memory _creatorId, string memory _content) public {
        require(bytes(_creatorId).length > 0, "Creator ID cannot be empty");
        require(bytes(_content).length > 0, "Content cannot be empty");

        uint128 _postId = uint128(posts.length);

        Post memory newPost = Post({
            id: _postId,
            creatorId: _creatorId,
            content: _content,
            active: true
        });

        posts.push(newPost);
        emit PostCreated(_postId);
    }

    function getPost(uint128 _id) public view returns (uint128 id, string memory, string memory, bool) {
        require(_id < posts.length, "Post does not exist");

        Post storage post = posts[_id];
        return (post.id, post.creatorId, post.content, post.active);
    }

    function getPosts() external view returns (Post[] memory) {
        return posts;
    }

    function activatePost(uint128 _id) public {
        require(_id < posts.length, "Post does not exist");

        Post storage post = posts[_id];
        post.active = true;
    }

    function deactivatePost(uint128 _id) public {
        require(_id < posts.length, "Post does not exist");

        Post storage post = posts[_id];
        post.active = false;
    }

    function setPostContent(uint128 _id, string memory _content) public {
        require(_id < posts.length, "Post does not exist");
        require(bytes(_content).length > 0, "Content cannot be empty");

        Post storage post = posts[_id];
        post.content = _content;
    }
}
