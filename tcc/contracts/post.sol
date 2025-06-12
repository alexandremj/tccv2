// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Chain {
    struct Post {
        uint128 id;
        string creatorId;
        string content;
        bool active;
        uint256 creationTime;
        uint256 updateTime;
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
            active: true,
            creationTime: block.timestamp,
            updateTime: block.timestamp
        });

        posts.push(newPost);
        emit PostCreated(_postId);
    }

    function getPost(uint128 _id) public view returns (uint128 id, string memory, string memory, bool, uint256, uint256) {
        require(_id < posts.length, "Post does not exist");

        Post storage post = posts[_id];
        return (post.id, post.creatorId, post.content, post.active, post.creationTime, post.updateTime);
    }

    function getPosts() external view returns (Post[] memory) {
        return posts;
    }

    function activatePost(uint128 _id) public {
        require(_id < posts.length, "Post does not exist");

        Post storage post = posts[_id];
        post.active = true;
        post.updateTime = block.timestamp;
    }

    function deactivatePost(uint128 _id) public {
        require(_id < posts.length, "Post does not exist");

        Post storage post = posts[_id];
        post.active = false;
        post.updateTime = block.timestamp;
    }

    function setPostContent(uint128 _id, string memory _content) public {
        require(_id < posts.length, "Post does not exist");
        require(bytes(_content).length > 0, "Content cannot be empty");

        Post storage post = posts[_id];
        post.content = _content;
        post.updateTime = block.timestamp;
    }
}
