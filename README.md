# DeSearch
## Inspiration
As freshmen who just left their parents, we know how important it is to filter the internet for clean and impressionable search results during our younger days. With widespread access to the internet, children can not only access sites they shouldn't see at that age, but the data they access will also influence how they think. To encourage children to form their own opinions, we developed a search engine built specifically to filter out inappropriate information and propagate with unbiased, educational search results. 

## What it does
DeSearch works like any other search engine with a search field to input key words that will subsequently generate impartial results that match those keywords. Furthermore, we add child-friendly functionality by blocking some sites, and prioritizing more positive and educational topics while straying away from more addictive and harmful platforms.

## How we built it
The web app was built using Django, JavaScript, HTML, and CSS. The backend was built using Python and NLTK.

## Challenges we ran into
In order to build a proper search engine, it required building a web crawler that can scour the Internet. Making it fast enough for usability, while also finding the right sites and not going in deep searches in useless websites (like the Twitter help section), was difficult.

Our initial idea involved adding blockchain decentralization to protect user privacy and enhance the user experience by adding a recommendation system. However, we were unable to find an easy way to integrate our blockchain contracts (both NEAR and Solana) into our search engine code. For the sake of future improvement, we still included our Rust and Seahorse contracts that would have been integrated with our app.

Finally, finding an optimal heuristic that removes useless or damaging websites required a lot of research in NLP models and how they work.

## Accomplishments that we're proud of
Every aspect of this project was new to us, and we managed to deal with these new problems fairly efficiently. Getting a fully functional web app that can directly assist children was a significant achievement alone. Furthermore, learning basic Rust and gaining experience with Blockchain development was also exciting. 

## What we learned
We learned how to build a web crawler and search engine, organize information by polarity and validity, and filter out content that meets a certain criteria. Even though they didn't end up working in our app in the end, we still learned to work with a database on a blockchain and how to code in Rust and Seahorse.

## What's next for DeSearch
As of now, the search engine is still slow when you try to get more results by clicking the next page, so finding a more efficient web crawler will allow for greater usability. We would also like to finish implementing the decentralized aspect of our project, as it would greatly improve its functionality and add additional purpose to using our search engine. We also might consider integrating it with the Graph on Ethereum because of their fast lookup times.
