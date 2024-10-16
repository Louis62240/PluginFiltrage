<template>
    <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 p-8">
      <div class="max-w-7xl mx-auto">
        <h1 class="text-5xl font-extrabold mb-12 text-center">
          <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
            Fil d'actualité
          </span>
        </h1>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div v-for="tweet in tweets" :key="tweet.id" 
               :class="['rounded-3xl overflow-hidden shadow-lg transition-all duration-500 transform hover:scale-105', 
                        tweet.isValid ? 'bg-gradient-to-br from-green-50 to-emerald-100' : 'bg-gradient-to-br from-red-50 to-rose-100']">
            <div class="p-6">
              <div class="flex items-center mb-4">
                <img :src="tweet.authorAvatar" :alt="tweet.author" class="w-16 h-16 rounded-full mr-4 border-4" 
                     :class="tweet.isValid ? 'border-green-400' : 'border-red-400'">
                <div>
                  <h3 class="font-bold text-xl" :class="tweet.isValid ? 'text-green-800' : 'text-red-800'">{{ tweet.author }}</h3>
                  <p class="text-sm" :class="tweet.isValid ? 'text-green-600' : 'text-red-600'">@{{ tweet.username }}</p>
                </div>
                <span :class="['ml-auto px-4 py-2 text-sm font-semibold rounded-full transition-all duration-300', 
                               tweet.isValid ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800']">
                  {{ tweet.isValid ? 'Tweet Valide' : 'Tweet Non Valide' }}
                </span>
              </div>
              <p class="text-lg leading-relaxed mb-4" :class="tweet.isValid ? 'text-green-900' : 'text-red-900'">{{ tweet.content }}</p>
              <div v-if="tweet.image" class="mb-4 rounded-xl overflow-hidden">
                <img :src="tweet.image" :alt="'Image pour ' + tweet.content" class="w-full h-56 object-cover transition duration-500 hover:scale-110">
              </div>
              <div class="flex items-center justify-between text-sm">
                <div class="flex space-x-6">
                  <button @click="likeTweet(tweet)" class="flex items-center space-x-2 transition-colors duration-300 focus:outline-none"
                          :class="tweet.isValid ? 'hover:text-green-700' : 'hover:text-red-700'">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="{'fill-current': tweet.liked}" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                    </svg>
                    <span>{{ tweet.likes }}</span>
                  </button>
                  <button @click="retweet(tweet)" class="flex items-center space-x-2 transition-colors duration-300 focus:outline-none"
                          :class="tweet.isValid ? 'hover:text-green-700' : 'hover:text-red-700'">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="{'fill-current': tweet.retweeted}" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>{{ tweet.retweets }}</span>
                  </button>
                </div>
                <span :class="tweet.isValid ? 'text-green-600' : 'text-red-600'">{{ tweet.date }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'TweetDisplay',
    data() {
      return {
        tweets: [
          {
            id: 1,
            author: 'John Doe',
            username: 'johndoe',
            authorAvatar: 'https://picsum.photos/id/1/200',
            content: 'Vue.js 3 est incroyable ! J\'adore la nouvelle Composition API et les performances améliorées. Qui d\'autre l\'utilise déjà ? 🚀 #vuejs #webdev',
            isValid: true,
            likes: 42,
            retweets: 10,
            date: 'Il y a 2 min',
            image: 'https://picsum.photos/id/0/500/300',
            liked: false,
            retweeted: false
          },
          {
            id: 2,
            author: 'Troll Account',
            username: 'trolluser',
            authorAvatar: 'https://picsum.photos/id/2/200',
            content: 'Ce tweet contient des insultes et du contenu inapproprié. Il ne respecte pas les règles de la communauté et devrait être signalé.',
            isValid: false,
            likes: 3,
            retweets: 1,
            date: 'Il y a 15 min',
            liked: false,
            retweeted: false
          },
          {
            id: 3,
            author: 'Dev Guru',
            username: 'devguru',
            authorAvatar: 'https://picsum.photos/id/3/200',
            content: 'Tailwind CSS + Vue.js = Une combinaison imbattable pour créer des interfaces utilisateur magnifiques et réactives ! Voici un exemple de ce que j\'ai créé récemment. Qu\'en pensez-vous ? 💙💚 #TailwindCSS #VueJS',
            isValid: true,
            likes: 88,
            retweets: 23,
            date: 'Il y a 1h',
            image: 'https://picsum.photos/id/180/500/300',
            liked: false,
            retweeted: false
          },
        ]
      }
    },
    methods: {
      likeTweet(tweet) {
        if (!tweet.liked) {
          tweet.likes++;
          tweet.liked = true;
        } else {
          tweet.likes--;
          tweet.liked = false;
        }
      },
      retweet(tweet) {
        if (!tweet.retweeted) {
          tweet.retweets++;
          tweet.retweeted = true;
        } else {
          tweet.retweets--;
          tweet.retweeted = false;
        }
      }
    }
  }
  </script>