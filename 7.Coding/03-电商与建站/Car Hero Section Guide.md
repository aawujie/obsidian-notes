---
notion-id: 22c78d23-e296-8039-a92d-f54458f91036
Tags: []
Last edited time: 2025-10-12T14:55:00
Verification: unverified
Owner:
  - 杰 吴
---
![[Screenshot_2025-07-10_at_4.16.31_PM.png]]

Remix link: [https://nest-hero-road.lovable.app](https://nest-hero-road.lovable.app/)

Bg video link: [https://drive.google.com/file/d/1CmvJ3WkkZDbH3denaPOH-KSdoScddcE-/view?usp=sharing](https://drive.google.com/file/d/1CmvJ3WkkZDbH3denaPOH-KSdoScddcE-/view?usp=sharing)

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

- 5 video series
- Daily support and feedback
- Weekly leaderboard rewards
- Opportunities to work with my agency [creme.digital](https://creme.digital/prajwal)

All for $35/month (15 spots left).

If you’re serious about building, **join us now**:

👉 [skool.com/ai-mvp-builders/about](https://www.skool.com/ai-mvp-builders/about)

---

## 🧠 Step 1: MidJourney Video Generation Prompt

![[Resources/images/7.Coding/03-电商与建站/imgs/image.png]]

Usually, i create my own images inside midjourney
but this time, i found a solid inspiration from @santu_design on X


I took a screenshot of the layout and dropped it into midjourney
then used the prompt below to turn it into a video


**Midjourney video prompt**
”Animate vintage Volkswagen Beetle move forward along the dusty road while maintaining a constant distance between the camera and the car, as if the camera is tracking it smoothly. The background landscape (fields, tree, hills, and sky) should shift subtly to simulate forward motion through the savannah during sunset. Keep the lighting consistent with the warm golden hour tones. Add slight movement to the grass to enhance realism, and subtle dust trail behind the car.”

---

## ☁️ Lovable Base Prompt

Create a full React functional component named HeroSection with the following exact details:

The entire section fills minimum full viewport height and full width, with overflow hidden.

A video background absolutely positioned covering entire section, with these exact settings:

autoPlay, muted, loop, playsInline

Video source: https://res.cloudinary.com/[YOUR_URL_HERE]

Video should fill full height and width, object-cover style.

On top, content container with relative z-index:

Header with site title "Nest" in Manrope font, font weight normal, size text-2xl on mobile, text-3xl on large screens, color class text-hero-text

Navigation with links: "Community", "Notes", "Reach Out"

Links are text-sm font-light by default, text-base on large screens

On hover, text color changes to nest-amber with smooth transition 300ms

The header items fade in with animate-fade-in with 0.2s delay for nav

Main content area:

Two headline lines:

"Where the Road"

"Slows Down."

Both lines use Manrope font, font-normal weight, text sizes scaling from 4xl (mobile) to 6xl (xl screens), color text-hero-text, leading-tight line height

Fade-in animation with 0.4s delay

Subheading paragraph below headline:

Text: Quiet retreats and grounded places, hosted by people who care. No itineraries. No rush. Just space to be where you are.

Max width 2xl, text-sm, color text-hero-text-subtle with 80% opacity, leading relaxed

Fade-in animation with 0.6s delay

Call-to-action button:

Use a button styled as variant "cta", size "lg"

Background white, text slate-900, on hover background white with 90% opacity

Button text: "Start the Journey" followed by a right arrow icon (ArrowRight from lucide-react) with horizontal translate on hover

Fade-in animation with 0.8s delay

Footer:

Left: Partner logos image from /lovable-uploads/07c6762e-8886-43f0-bc8e-e2a4d0744bfa.png, opacity 60%, height 32, width auto, fade-in delay 1s

Center: vertical line 1px wide, 16 height, background bg-hero-text-subtle, 40% opacity, fade-in delay 1.1s

Right: Quote text "Stories, reflections, and grounded thoughts from the quiet side of the road, where days stretch longer and the noise fades out."

Text base size, color text-hero-text-subtle, opacity 80%, leading relaxed, max width md, fade-in delay 1.2s

All fonts are font-manrope and font weights are font-normal except for navigation which is font-light.

Spacing matches the provided code: header and footer paddings 8 on mobile, 12 on large screens; main content padding horizontal 8 mobile, 12 large, padding top 16.

Include the fade-in animation classes and exact delay inline styles as described.

The component imports and uses Button from "@/components/ui/button" and ArrowRight from "lucide-react".

The entire code is formatted as shown in the example, fully functional React component with JSX.


