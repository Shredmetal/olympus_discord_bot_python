import random

# List of GIF URLs
gif_urls = [
    "https://cdn.discordapp.com/attachments/1171360820085674054/1253373883785023508/image0.gif?ex=6676f064&is=66759ee4&hm=bdad33ca09e4c29fc6323706093504bfc146149f5857b4b61c21551eda784104&",
    "https://cdn.discordapp.com/attachments/1171360820085674054/1253373970724425758/image0.gif?ex=6676f079&is=66759ef9&hm=266a23f0cea8ac898bcdacad9d4f11dcf7881bb05771e1e0a4a7b5bb009b0a7e&",
    "https://media.discordapp.net/attachments/1171360820085674054/1253374145916567613/image0.gif?ex=6676f0a2&is=66759f22&hm=73b612d6b6df9ffc342e1b91748d96e60eec32343912f9f2b6f16f84a0fa9912&=",
    "https://media.discordapp.net/attachments/1171360820085674054/1253374146683994182/image2.gif?ex=6676f0a3&is=66759f23&hm=794113b2dd41ebf27167adc156502991c72313232fbe6358d1abfc1eeb8d6c20&=",
    "https://media.discordapp.net/attachments/1171360820085674054/1253374147019669626/image3.gif?ex=6676f0a3&is=66759f23&hm=f1320a11ddde8c752f40748ef36fea77d990e9a0a9d41a77fb6e33d64a17b845&="
]

def get_random_gif():
    return random.choice(gif_urls)