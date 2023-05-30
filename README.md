<a name="readme-top"></a>
<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/5NT-1/WanderBuddy">
    <img src="images/hero.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">WanderBuddy</h3>

  <p align="center">
    WanderBuddy is a traveling tool aimed to help tourists share their adventures.
    <br />
    <a href="https://github.com/5NT-1/WanderBuddy"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/5NT-1/WanderBuddy">View Demo</a>
    ·
    <a href="https://github.com/5NT-1/WanderBuddy/issues">Report Bug</a>
    ·
    <a href="https://github.com/5NT-1/WanderBuddy/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python]][Python-url]
* [![Telegram][Telegram]][Telegram-url]
* [![Supabase][Supabase]][Supabase-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Verify that pip is installed
  ```sh
  pip --version
  ```

* Verify that supabase is installed
  ```sh
  supabase --version
  ```
  You may refer to [this link](https://supabase.com/docs/guides/getting-started/local-development) for instructions to install supabase

### Installation

1. Get a Bot Token from Telegram's @BotFather. You may follow the instructions here ["Obtaining your Bot Token"](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
2. Clone the repo
   ```sh
   git clone https://github.com/5NT-1/WanderBuddy.git
   ```
3. Install pip dependencies
   ```sh
   cd WanderBuddy
   pip install -r requirements.txt
   ```
4. Make a local copy of environment variables
   ```sh
   cp .env.example .env
   cp .env.local.example .env.local
   ```
5. Enter your BOT TOKEN, Supabase credentials in `.env` and `.env.local`
   ```sh
   BOT_TOKEN=<BOT_TOKEN_HERE>
   ...
   ```
   You will also need the FRONTEND_URL if you're hosting a frontend
6. Start up a local database
   ```sh
   supabase start
   ```
6. Start up the frontend server 
   ```sh
   cd supabase-react && npm run dev
   ```

6. Start up the telegram-bot
   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

_For more examples, please refer to the [Documentation](https://example.com)_

1. Start a new chat with your Telegram Bot with `/start`.
2. The Bot will prompt you to start a new Trip! 
3. After adding the name of the trip, the Bot will prompt you to create a new route.
4. Once the route has been created, you can now start tracking your adventures!
- You can send a location to mark a new checkpoint in your journey
- You can send an image to store your memories at the current location
- Whenever you're ready to move on, you can use the `/next` and `/prev`
5. After you're done with your journey, feel free to share it with your friends!
- Use the `/share_trip` [friend's telegram username] to share.
- Your friend can use the `/follow` command to import it into their own collection!
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/5NT-1/WanderBuddy/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Project Link: [https://github.com/5NT-1/WanderBuddy](https://github.com/5NT-1/WanderBuddy)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Devpost](https://lifehack-23.devpost.com/) We would like to thank NUS Students' Computing Club, and the organising committee for organising LifeHack'2023
* [Standard Chartered](https://www.sc.com/sg/) for sponsoring the Hackathon
* [Other distinguished sponsors](https://lifehack-website.web.app/) for sponsoring the Hackathon

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/5NT-1/WanderBuddy.svg?style=for-the-badge
[contributors-url]: https://github.com/5NT-1/WanderBuddy/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/5NT-1/WanderBuddy.svg?style=for-the-badge
[forks-url]: https://github.com/5NT-1/WanderBuddy/network/members
[stars-shield]: https://img.shields.io/github/stars/5NT-1/WanderBuddy.svg?style=for-the-badge
[stars-url]: https://github.com/5NT-1/WanderBuddy/stargazers
[issues-shield]: https://img.shields.io/github/issues/5NT-1/WanderBuddy.svg?style=for-the-badge
[issues-url]: https://github.com/5NT-1/WanderBuddy/issues
[license-shield]: https://img.shields.io/github/license/5NT-1/WanderBuddy.svg?style=for-the-badge
[license-url]: https://github.com/5NT-1/WanderBuddy/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Telegram]: https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white
[Telegram-url]: https://telegram.org/?setln=en
[Supabase]: https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white
[Supabase-url]: https://supabase.com/
