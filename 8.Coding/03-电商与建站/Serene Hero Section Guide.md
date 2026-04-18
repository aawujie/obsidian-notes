---
notion-id: 22b78d23-e296-80af-8e25-faa415f9f670
Tags: []
Last edited time: 2025-10-12T14:55:00
Verification: unverified
Owner:
  - 杰 吴
---
![[Screenshot_2025-07-07_at_2.08.41_PM.png]]

Remix link: [https://preview--edge-of-silence-calm.lovable.app/](https://preview--edge-of-silence-calm.lovable.app/)

Bg video link : [https://drive.google.com/file/d/1OZ1wF_t1jblNAIjHYPjZdWob3EN7milA/view?usp=sharing](https://drive.google.com/file/d/1OZ1wF_t1jblNAIjHYPjZdWob3EN7milA/view?usp=sharing)

## Steps (Exact Prompts Below)

1. **Start with Dribbble / Behance / Pinterest / X for visual inspiration**
Browse them and pick an image layout or vibe you love.
2. **Use ChatGPT to create a detailed prompt**
Drop the image into ChatGPT. Ask it to describe the visual and generate a prompt you can use to recreate something similar.
3. **Generate an original image using AI tools**
Paste that prompt into a tool like Ideogram, Leonardo, or ChatGPT for image generation.
Customize it with your own color palette, brand vibe, and theme.
4. **Bring the image to life inside MidJourney**
Upload your AI-generated image into MidJourney.
Use ChatGPT again to help you craft a strong prompt that animates or enhances the visual feel.
Paste that prompt into MidJourney and generate a video version of your image.
5. **Host the video on Cloudinary**
Once your video is ready, upload it to Cloudinary and copy the direct video URL.
6. **Use it in Lovable as your hero background**
Inside Lovable, paste the Cloudinary video link as the hero section background.
This adds motion, vibe, and originality to your landing page.

---

### **Want to build faster with AI?**

This is just one workflow I teach inside **AI MVP Builders, **a private community for devs using AI to ship real products.

Inside, you get:

- 4 video series
- Daily support and feedback
- Weekly leaderboard rewards
- Opportunities to work with my agency [creme.digital](https://creme.digital/prajwal)

All for $35/month (15 spots left).

If you’re serious about building, **join us now**:

👉 [skool.com/ai-mvp-builders/about](https://www.skool.com/ai-mvp-builders/about)

---

## 🧠 Step 1: MidJourney Video Generation Prompt

![[PHOTO-2025-07-07-13-32-31.jpg]]

Usually, i create my own images inside midjourney
but this time, i found a solid inspiration from @santu_design on X

Inspiration post:

[https://x.com/santu_design/status/1940728505509335170](https://x.com/santu_design/status/1940728505509335170)

I took a screenshot of the layout and dropped it into midjourney
then used the prompt below to turn it into a video


**Midjourney video prompt**
”A serene cinematic animation of a monk meditating on the edge of a rocky cliff at dawn, with a glowing full moon on the horizon and a vast waterfall flowing behind him. The water should be visibly moving, cascading powerfully and continuously into mist below. The sky has a soft warm gradient from teal to peach, with light fog drifting across. The scene is peaceful, atmospheric, and dreamlike.”

---

## ☁️ Lovable Base Prompt

Create a React landing page with a fullscreen video background, fixed top navigation bar, and centered hero content, styled precisely using Tailwind CSS with the following specifications:

Background Video

A fullscreen video fills the entire viewport (100vw × 100vh) using CSS object-cover to maintain aspect ratio and crop overflow.

The video is autoplaying, muted, looping, and plays inline.

Video source URL:
[https://res.cloudinary.com/doevp9obh/video/upload/v1751630378/social_u7865913127_httpss.mj.runfy9I6hP3bjY_A_serene_cinematic_anima_3732f431-944f-4ee3-9b66-c82c1462de47_1_vjttzg.mp4](https://res.cloudinary.com/doevp9obh/video/upload/v1751630378/social_u7865913127_httpss.mj.runfy9I6hP3bjY_A_serene_cinematic_anima_3732f431-944f-4ee3-9b66-c82c1462de47_1_vjttzg.mp4)

Overlay a subtle black layer on top of the video with 20% opacity (bg-black/20) covering the entire viewport to enhance text readability.

Page Layout

The base page background color is solid black (bg-black) behind the video.

Hero content container is vertically and horizontally centered within the viewport (flex items-center h-screen).

Max container width for content is max-w-7xl with horizontal padding of px-6.

The hero content block inside is max width max-w-2xl and includes a fade-in animation.

Navigation Bar

Fixed at the top of the viewport (fixed top-0 left-0 right-0), spanning full width.

Background is semi-transparent black with 10% opacity (bg-black/10) and a slight backdrop blur (backdrop-blur-sm).

Vertical padding py-4 and horizontal padding px-6.

Inside nav is a flex container (flex justify-between items-center) to space the logo on the left and navigation links on the right.

Logo text: "Calm" in white, serif font font-playfair, size text-xl, normal weight.

Navigation links: "Our Mission", "Support Us", "Contact", and language selector "EN" with a downward chevron icon (size 14) from lucide-react.

Nav links styled with white text at 90% opacity (text-white/90), font font-inter, size text-sm, font weight light (font-light), spaced with gap-8.

Hover effect on links and language selector: text becomes pure white (hover:text-white), scale up slightly (hover:scale-105), smooth transition on colors and scale (transition-colors duration-300), cursor pointer on language selector.

Hero Content Text

Heading uses font-playfair serif font, white color, font sizes responsive from text-4xl on small screens to text-6xl on large, font weight normal, tight letter spacing (tracking-tight), margin bottom 8.

The word “Silence” in the heading is italicized.

Subheading paragraph uses font-inter sans-serif font, color text-gray-200, font size responsive from text-lg to text-xl, light font weight, line height relaxed, margin bottom 12, max width max-w-xl.

Call-to-action button below paragraph: white background with dark gray text (text-gray-900), font font-inter medium weight, padding horizontal 6, vertical 3, rounded corners large (rounded-lg), base font size (text-base).

Button hover states: background lightens to gray-100 (hover:bg-gray-100), scales up (hover:scale-105), subtle shadow (hover:shadow-lg), smooth transitions (transition-all duration-300).

Footer Text

Positioned absolutely near bottom center (absolute bottom-6 left-0 right-0).

Container with max width max-w-7xl mx-auto px-6, flex container spaced between left and right items.

Text uses font-inter, white color with 70% opacity (text-white/70), font size extra small (text-xs), light font weight.

Z-Index Layering

Video background and overlay at lowest z-index (z-0).

Hero content and footer text above overlay (z-10).

Navigation bar fixed on top with highest z-index (z-50).

Fonts

Use Playfair Display for headings and logo text (serif, elegant).

Use Inter for paragraphs, buttons, and navigation links (sans-serif, clean and modern).

Use font weights as specified: normal for headings, light for nav links and paragraphs, medium for buttons.


