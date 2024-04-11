css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #067FD0
}
.chat-message.bot {
    background-color: #E63B60
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.etsystatic.com/39477223/r/il/58f254/4621727445/il_fullxfull.4621727445_mbda.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.freepik.com/free-vector/happy-girl-sitting-floor-hugging-knees-with-cat-cartoon-art-illustration_56104-665.jpg?size=626&ext=jpg&ga=GA1.1.735520172.1711411200&semt=ais">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''