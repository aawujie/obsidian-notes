---
title: "Differential Equations: The Language of Change — YouTube 转录"
type: transcript
created: 2026-05-23
source: https://www.youtube.com/watch?v=vTTlzmCRwU4
tags: [数学, 微分方程, 动力系统, 神经科学, 转录]
---

# Differential Equations: The Language of Change

**频道**: Artem Kirsanov
**时长**: 23:23
**发布日期**: 2024-10-08
**链接**: https://www.youtube.com/watch?v=vTTlzmCRwU4
**转录工具**: faster-whisper large-v3 (language=en, CPU int8)

---

## 完整文案（纯净版）

Imagine zooming in on a single neuron in your brain. At first glance, it might seem like a simple device. It receives inputs, and if they are strong enough, it fires an output impulse. But this view misses one of the most fascinating aspects of neural behavior — its intricate dynamics in time. Neurons are not static input-to-output machines. They are sophisticated temporal computers, changing their state and responsiveness from moment to moment.

How a given neuron responds to input depends not only on that very input, but also on what this neuron was doing a millisecond ago, a second ago, or even minutes in the past. This temporal complexity is the key to understanding how the brain generates such a rich variety of thoughts and behaviors.

A beautiful branch of mathematics that describes exactly these phenomena is called dynamical systems theory. It deals with differential equations. But despite this intimidating name, most of the insights it offers actually can be grasped without a single formula, simply by looking at pictures.

In this video, which is the first one in upcoming series, we'll lay the foundation. We'll introduce what differential equations even are, and discuss important concepts such as equilibrium points, phase portraits, and limit cycles. And in later videos, we'll take the groundwork established today and apply it to neuronal dynamics, to gain a geometric intuition behind phenomena such as spiking, bursting, or adaptation. If you're interested, stay tuned.

---

At its core, dynamical systems theory is about studying how things change over time. A system, the thing that is changing, can be pretty much anything. A neuron firing, a population of animals interacting, a leaf floating in the water, or even the global climate. The key is having a way to describe the system's state at any given point. This is where the idea of state variables comes in. These are real numbers that, when known, fully determine the state of the system, everything that you might care about.

For instance, consider a ball moving through a three-dimensional space. To fully describe its state at any given time point, assuming you know all the forces that act on it, like gravity or air drag, all you need to know are the three coordinates x, y, and z. These are the three numbers that describe its position in space, as well as the three components of the velocity, how fast the ball is moving in those three directions. Once you have those six numbers, you fully know the state of the system in the sense that you can unambiguously predict its trajectory arbitrarily far into the future.

And for a simple pendulum, you only need two state variables, the angle from the vertical and the angular velocity. But what about more complex systems? How can you even know what state variables are? Well, it depends on the particular system and the level of abstraction you want to characterize it on. After all, these are all models designed to describe a particular aspect of the real world while discarding all others as irrelevant.

For instance, the two state variables for a pendulum are only justified if we allow ourselves to approximate the pendulum as a single point. While if we care about its rotation or its deformations or the temperature, we might need a larger set of state variables. In the case of a neuron, when we are talking about its computations, we really care about the electrical properties while discarding other things as irrelevant, such as the concentration of sugar floating around or the DNA being repaired. Meanwhile, for a biochemist who wants to describe and model these very phenomena, it is the other way around. As you can see, choosing these state variables, what to describe and what to throw away, is kind of an art of its own.

We'll talk about what the state variables for a neuron are a bit further in the series. But for now, let's introduce the formalism of differential equations that describe how these state variables actually change over time.

---

Imagine you are tracking a population of bacteria in a petri dish. Initially, you start with a thousand and then you count them every hour. After a few hours, you might see a pattern like this. There is clearly some relationship here. It looks like the number of bacteria, which is the only one state variable, doubles every hour. We can express this mathematically in the following way, where n is the number of bacteria at time t.

Now, here's a question for you. What would the population size be in between those hourly measurements? For example, if you only came into the room after just 30 minutes. Well, we know that bacteria don't wait for the one-hour mark to suddenly double. So, you can see that the population size is going to be continuously increasing. So, something must be happening in between those measurements. Your first guess might be that after 30 minutes, the population size will be exactly halfway between 1000 and 2000, so about 1500. But let's dig deeper.

To really understand what's going on, we need to think about how fast the population is growing. What we call the rate of change. Think of it like a speedometer for our bacteria population. Just like a car speedometer shows kilometers per hour how fast you're moving, our bacterial speedometer will show how fast the population is growing in terms of bacteria per unit time. We can denote this rate of growth with a little dot above n like this.

In our petri dish, each bacterium divides independently. That means that at any given moment, the rate with which new bacteria are appearing is proportional to the number of bacteria already there. We can write this as an equation. The constant k represents the fraction of the population that are dividing at any given moment, and it depends on things like temperature or food availability.

This simple-looking formula is actually a very big deal in mathematics. This is called a differential equation, and it relates a value of a quantity to its rate of change. Differential equations are the language of dynamical systems, describing how things change over time, from physics to neuroscience.

---

Let's zoom in even closer on this concept of a rate of change. In mathematics, we call it a derivative, and there is a special way of writing it as dn over dt, equivalent to the dot notation we used earlier. Imagine dn as a tiny change in the number of bacteria, and dt as a tiny step in time. The derivative dn over dt represents how much n changes when we take an infinitely small step dt into the future.

If you imagine the population size over time as a graph, then the derivative, the value of our speedometer at any given time, corresponds to the slope of the line tangent to the graph at that point. In the real world, of course, we cannot have a fraction of a bacterium. But it's useful to think of the population as changing smoothly and continuously, growing by very small amounts as you take very small time steps into the future. It lets us rely on the process of calculus that describes and analyzes continuous processes.

Now, this is where things get interesting. When we move from pure math to the practical world of computation and modeling, we need to make a subtle but very important shift. Instead of dealing with infinitely small changes, we'll work with still small but measurable steps. To highlight this difference, we'll use the symbol delta instead of d. So, delta n represents a small, but not infinitesimal, change to n. And delta t is a small, but not infinitely small step in time. This shift is at the heart of numerical methods, which we'll rely on throughout the video series.

Let's see how it works in practice. Imagine we decide to measure our population every 5 minutes instead of every hour. 5 minutes is small enough that we can reasonably assume the rate of change doesn't vary much during that time. This corresponds to the idea that if you zoom in close enough on the graph of a curve, it starts to look like a straight line.

Let's work through an example. Suppose we start with 1000 bacteria, and we know that k equals 1 when time is measured in hours. This means that our rate of change equation becomes the following. So, when we have 1000 bacteria, they are multiplying at a rate of 1000 bacteria per hour, or about 17 every minute. After 5 minutes, we estimate the population size to become 1085 bacteria instead. Now we update our rate of change based on this new population size to become 18 bacteria per minute instead of 17. So, we can estimate the population size for the next 5-minute time step. And we can keep repeating this process to estimate the population for any future time.

This is the essence of solving differential equations with numerical methods.

Those of you who immediately recognize the equation for exponential growth, might be wondering why we are spending so much time on this computational approach when this particular equation can be much more easily solved analytically. And you'd be right, but the reason is simple. For most of the differential equations out there, including the ones governing the neuronal dynamics, such an analytical solution that would allow us to jump ahead multiple computational steps simply does not exist. Numerically, however, we can solve basically any differential equation imaginable.

There are several important differences between those two approaches. The numerical solution requires us to perform many update steps, multiplications and additions to arrive at the result. Getting estimates for later time demands more computational effort. Unlike an analytical solution, we don't have an explicit formula where we can simply plug in values and get a result instantly.

Another crucial aspect is the finite precision of our method. In our example, we used five-minute steps. But for greater accuracy, we might need to decrease the step size, perhaps updating our estimate every minute, or even every second. The more accurate we want our answer to be, the more computation it requires.

There is one more important point to consider. In our computations, we assumed that we somehow know the underlying value k that relates the rate of change to the value of the population size. In reality, however, we don't usually have access to parameters like these. Instead, we collect data similar to the table we had in the beginning, and we might need to run multiple computations to try different values of parameters to find the one that would fit our data best. This process too involves finite precision, so inaccuracies are inevitable.

Now that we've established what differential equations actually are and how to solve them, let's talk about the geometric intuition behind dynamical processes and how these equations can help us gain insight into the behavior of the system.

---

To introduce key concepts, let's explore another fundamental model in biology. Now we're stepping into the world of coupled differential equations, where we will have multiple state variables and the rate of change of each depends on all the others. Consider the interactions between co-existing populations in a predator-prey model, often illustrated with rabbits and foxes.

As the rabbit population grows, foxes have more food, leading to an increase in their numbers. However, more foxes means more rabbits get eaten, causing the rabbit population to decline. With fewer rabbits, the fox population shrinks, allowing rabbits to reproduce, and the cycle continues. This intuitive understanding is certainly compelling, but can we build a simple mathematical model that would describe these oscillations?

Let's start by defining our variables. x will denote the number of rabbits, and y will mean the number of foxes. We are aiming for a system of equations in this form, where f and j are functions relating the rate of change of each variable to the overall state of the system. In reality, those functions can contain countless complexities and dependencies on other factors. However, we are seeking the simplest mathematical model that captures the essence of such oscillations.

Let's start with our prey population. Rabbits reproduce at a rate proportional to their population, giving us the term ax, where a is the positive net growth rate. Note that there is also an analogous rate for natural deaths proportional to the population size, but here we are assuming that the birth rate significantly exceeds the net growth rate, so the total population growth rate is positive.

Rabbits also get eaten by foxes. We account for this with an interaction term minus b times xy in the equation for x. This term is proportional to the product of x and y, representing the probability of rabbits and foxes encountering each other, multiplied by the fraction of encounters that lead to rabbits being caught. Thus, our equation for the prey population is: dx/dt = ax - bxy.

Now for the predators. Foxes benefit from eating rabbits, converting a proportion of that energy into reproduction. This gives us the positive interaction term. We also include a term for natural deaths, which typically outweighs natural births for predators in the absence of prey. This results in the differential equation for y: dy/dt = cxy - dy.

This simple model of two coupled differential equations is a very powerful tool for exploring the geometry of dynamical systems.

---

Now, how do we solve this system? As before, we'll rely on numerical methods. Suppose we know the values for all the four parameters a, b, c, and d. Given an initial state, we can compute the derivatives, make incremental changes to x and y, and repeat this process. This would give us two curves showing how each variable changes over time.

However, to gain a deeper insight, let's visualize our data differently. Instead of plotting time as a horizontal axis and population size as the vertical, imagine a coordinate plane where x-axis represents the number of rabbits and y-axis represents the number of foxes. Notice that there is no time dimension here. Each point on this plane represents a possible state of our system at a given instant, with time governing the trajectory of switching between the states.

Such a coordinate plane that corresponds to different states of the system as a whole is known as the phase space. In this phase space, each point has two corresponding rates of change, the instantaneous velocities of the rabbit and fox populations. We can represent these as vectors, little arrows coming from each point, with the horizontal component of the arrow given by the derivative of x, and the vertical given by the derivative of y.

This graphically shows the mapping between the system's state (x-y coordinates) and its rates of change. If we plot these vectors for many points, we create a vector field, showing how the system's evolution flows from any starting point. This is known as the phase portrait. With such visualization, we can gain qualitative insight into the system's behavior without doing precise number crunching. We can simply visually follow the arrows to get a feeling for the trajectory.

---

With that model in hand, let's see what interesting dynamics we can observe.

First, let's look for special points within our phase space where the system settles into balance. These are known as equilibrium points, and they correspond to both derivatives being equal to zero. If it falls into one of those states, it will remain there forever, as there is no mechanism for it to get out.

Equilibrium points can be found by setting the right-hand side of our equations to zero, turning differential equations into a system of familiar algebraic equations with two unknowns that are numbers instead of functions. Solving this gives us two equilibrium points: (0, 0), which means that both populations are extinct — a trivial but mathematically valid solution. And there is another non-zero equilibrium, which means that there exists a balance between predators and prey. Now that's more interesting.

In our phase portraits, these equilibria appear as points where all arrows shrink to zero, indicating that once you reach that point, there is no way out. Rabbits and foxes will be exactly balancing each other out with no changes to the population dynamics.

But how does the system behave around these points?

Let's start with the origin. If we are slightly off of this point, let's say a few rabbits but no foxes, what happens? Well, our equations tell us that the population of rabbits will continue to grow exponentially, while the population of foxes remains zero. In the phase space, that looks like a trajectory moving right along the x-axis. The (0, 0) equilibrium is unstable. The slightest perturbation sends the system away. In the other direction, though, if we have a few foxes but no rabbits, their population will go down, approaching the point of extinction closer and closer, as there is no food for the foxes to reproduce.

Now, what about the non-zero equilibrium? If we start near that point and follow the arrows in our phase portrait, we see something remarkable. The populations cycle endlessly around the equilibrium, creating a closed loop. This behavior is called a limit cycle, and it will actually be fundamental when we talk about the excitability of neurons.

Notice that we never explicitly put any oscillations into our system of equations. There are no trig functions or circles in the initial description. Limit cycles emerge from this seemingly simple dynamic law of interaction between the two variables. And there isn't just one — there are infinitely many cycling orbits. Which one you will end up on depends on the initial conditions.

So far, we have fixed a particular set of parameters. Varying the values of a, b, c, and d doesn't fundamentally change the behavior of the system. It only affects the position of the non-zero equilibrium, as well as the exact shape and amplitude of the limit cycle oscillations.

Slightly modifying our system of equations to account for the limited availability of food to rabbits leads to another interesting behavior. In addition to the large number of cycles that can be realized depending on the initial condition, there is now a single stable equilibrium, which all trajectories converge to, defining the stable balance between rabbits and foxes.

---

As we have seen, even such a simple system as the predator-prey model can exhibit very rich and complex behaviors. The idea of a phase portrait gives us a powerful visual tool to understand these dynamics without getting lost in mathematics. Ideas such as the stability of equilibrium points and the emergence of limit cycles form the foundation of dynamical systems theory, applicable to a variety of fields.

Crucially, these same ideas can help us understand the intricate workings of the brain. Neurons, like the populations of rabbits and foxes, can be described as dynamical systems as well. The state variables might represent things like the membrane potential and the state of ion channels, instead of the population sizes. But all the underlying principles remain the same.

However, to truly understand the differential equations that govern the dynamics of a neuron, we will first have to dive into the world of cellular biophysics, which deserves a dedicated video. So stay tuned for that next adventure.

---

## 核心概念速览

| 概念 | 说明 |
|------|------|
| **动力系统** (Dynamical System) | 研究事物如何随时间变化的数学分支 |
| **状态变量** (State Variables) | 完全描述系统状态的实数值 |
| **微分方程** (Differential Equation) | 关联数量与其变化率的方程 |
| **导数** (Derivative) | 无穷小时间步长内的变化量 (dn/dt) |
| **数值方法** (Numerical Methods) | 用有限步长 Δt 近似求解微分方程 |
| **相空间** (Phase Space) | 以状态变量为坐标的平面/空间 |
| **向量场** (Vector Field) | 显示每个状态点变化方向 |
| **相图** (Phase Portrait) | 向量场 + 轨迹的可视化 |
| **平衡点** (Equilibrium Points) | 所有导数为零的特殊点 |
| **极限环** (Limit Cycle) | 系统围绕平衡点的闭合循环轨道 |

---

## 带时间戳的完整文案

> 以下为 faster-whisper large-v3 生成的逐段转录，包含精确时间戳。

Imagine zooming in on a single neuron in your brain. (0:00)

At first glance, it might seem like a simple device. It receives inputs, and if they are strong enough, it fires an output impulse. But this view misses one of the most fascinating aspects of neural behavior — its intricate dynamics in time. (0:03-0:18)

Neurons are not static input-to-output machines. They are sophisticated temporal computers, changing their state and responsiveness from moment to moment. (0:18-0:28)

How a given neuron responds to input depends not only on that very input, but also on what this neuron was doing a millisecond ago, a second ago, or even minutes in the past. This temporal complexity is the key to understanding how the brain generates such a rich variety of thoughts and behaviors. (0:29-0:48)

A beautiful branch of mathematics that describes exactly these phenomena is called dynamical systems theory. It deals with differential equations. But despite this intimidating name, most of the insights it offers actually can be grasped without a single formula, simply by looking at pictures. (0:49-1:07)

**1:08 — 微分方程基础**

In this video, which is the first one in upcoming series, we'll lay the foundation. We'll introduce what differential equations even are, and discuss important concepts such as equilibrium points, phase portraits, and limit cycles. And in later videos, we'll take the groundwork established today and apply it to neuronal dynamics, to gain a geometric intuition behind phenomena such as spiking, bursting, or adaptation. (1:08-1:33)

**1:43 — 什么是动力系统**

At its core, dynamical systems theory is about studying how things change over time. A system, the thing that is changing, can be pretty much anything. A neuron firing, a population of animals interacting, a leaf floating in the water, or even the global climate. (1:43-2:00)

**2:01 — 状态变量**

The key is having a way to describe the system's state at any given point. This is where the idea of state variables comes in. These are real numbers that, when known, fully determine the state of the system, everything that you might care about. (2:01-2:16)

**2:17 — 三维空间中的球**

For instance, consider a ball moving through a three-dimensional space. To fully describe its state at any given time point, assuming you know all the forces that act on it, like gravity or air drag, all you need to know are the three coordinates x, y, and z, as well as the three components of the velocity. Once you have those six numbers, you fully know the state of the system in the sense that you can unambiguously predict its trajectory arbitrarily far into the future. (2:17-2:55)

And for a simple pendulum, you only need two state variables, the angle from the vertical and the angular velocity. (2:56-3:03)

**3:03 — 模型是世界的抽象**

But what about more complex systems? How can you even know what state variables are? Well, it depends on the particular system and the level of abstraction you want to characterize it on. After all, these are all models designed to describe a particular aspect of the real world while discarding all others as irrelevant. (3:03-3:21)

**3:41 — 神经元的状态变量**

In the case of a neuron, when we are talking about its computations, we really care about the electrical properties while discarding other things as irrelevant, such as the concentration of sugar floating around or the DNA being repaired. As you can see, choosing these state variables, what to describe and what to throw away, is kind of an art of its own. (3:41-4:04)

**4:13 — 微分方程的形式化**

But for now, let's introduce the formalism of differential equations that describe how these state variables actually change over time. (4:13-4:21)

**4:21 — 细菌繁殖的例子**

Imagine you are tracking a population of bacteria in a petri dish. Initially, you start with a thousand and then you count them every hour. After a few hours, you might see a pattern like this. It looks like the number of bacteria doubles every hour. (4:21-4:41)

**4:50 — 测量间隔之间发生了什么？**

Now, here's a question for you. What would the population size be in between those hourly measurements? For example, if you only came into the room after just 30 minutes. Well, we know that bacteria don't wait for the one-hour mark to suddenly double. So, something must be happening in between those measurements. (4:50-5:13)

**5:25 — 变化率 (Rate of Change)**

To really understand what's going on, we need to think about how fast the population is growing. What we call the rate of change. Think of it like a speedometer for our bacteria population. We can denote this rate of growth with a little dot above n. (5:25-5:52)

**5:53 — 微分方程的定义**

In our petri dish, each bacterium divides independently. That means that at any given moment, the rate with which new bacteria are appearing is proportional to the number of bacteria already there. The constant k represents the fraction of the population that are dividing at any given moment, and it depends on things like temperature or food availability. (5:53-6:17)

This simple-looking formula is actually a very big deal in mathematics. This is called a differential equation, and it relates a value of a quantity to its rate of change. Differential equations are the language of dynamical systems, describing how things change over time, from physics to neuroscience. (6:18-6:38)

**6:38 — 导数的几何意义**

Let's zoom in even closer on this concept of a rate of change. In mathematics, we call it a derivative, and there is a special way of writing it as dn over dt. Imagine dn as a tiny change in the number of bacteria, and dt as a tiny step in time. The derivative dn over dt represents how much n changes when we take an infinitely small step dt into the future. (6:38-7:08)

If you imagine the population size over time as a graph, then the derivative corresponds to the slope of the line tangent to the graph at that point. (7:09-7:22)

**7:23 — 连续变化的近似**

In the real world, of course, we cannot have a fraction of a bacterium. But it's useful to think of the population as changing smoothly and continuously, growing by very small amounts as you take very small time steps into the future. It lets us rely on the process of calculus that describes and analyzes continuous processes. (7:23-7:46)

**7:47 — 从无穷小到有限步长**

Now, this is where things get interesting. When we move from pure math to the practical world of computation and modeling, we need to make a subtle but very important shift. Instead of dealing with infinitely small changes, we'll work with still small but measurable steps. To highlight this difference, we'll use the symbol delta instead of d. This shift is at the heart of numerical methods, which we'll rely on throughout the video series. (7:47-8:21)

**8:22 — 数值方法实战**

Let's see how it works in practice. Imagine we decide to measure our population every 5 minutes instead of every hour. 5 minutes is small enough that we can reasonably assume the rate of change doesn't vary much during that time. This corresponds to the idea that if you zoom in close enough on the graph of a curve, it starts to look like a straight line. (8:22-8:44)

Suppose we start with 1000 bacteria, and we know that k equals 1 when time is measured in hours. When we have 1000 bacteria, they are multiplying at a rate of 1000 bacteria per hour, or about 17 every minute. After 5 minutes, we estimate the population size to become 1085 bacteria. Now we update our rate of change based on this new population size to become 18 bacteria per minute instead of 17. And we can keep repeating this process to estimate the population for any future time. (8:47-9:33)

This is the essence of solving differential equations with numerical methods. (9:34-9:38)

**9:38 — 解析解 vs 数值解**

Those of you who immediately recognize the equation for exponential growth, might be wondering why we are spending so much time on this computational approach when this particular equation can be much more easily solved analytically. And you'd be right, but the reason is simple. For most of the differential equations out there, including the ones governing the neuronal dynamics, such an analytical solution that would allow us to jump ahead multiple computational steps simply does not exist. Numerically, however, we can solve basically any differential equation imaginable. (9:38-10:12)

**10:13 — 两种方法的差异**

There are several important differences between those two approaches. The numerical solution requires us to perform many update steps, multiplications and additions to arrive at the result. Getting estimates for later time demands more computational effort. Unlike an analytical solution, we don't have an explicit formula where we can simply plug in values and get a result instantly. (10:13-10:38)

**10:44 — 精度与步长的权衡**

Another crucial aspect is the finite precision of our method. In our example, we used five-minute steps. But for greater accuracy, we might need to decrease the step size, perhaps updating our estimate every minute, or even every second. The more accurate we want our answer to be, the more computation it requires. (10:44-11:01)

**11:02 — 参数估计的不确定性**

There is one more important point to consider. In our computations, we assumed that we somehow know the underlying value k. In reality, we don't usually have access to parameters like these. Instead, we collect data and we might need to run multiple computations to try different values of parameters to find the one that would fit our data best. This process too involves finite precision, so inaccuracies are inevitable. (11:02-11:34)

**11:40 — 几何直觉：捕食者-猎物模型**

Now that we've established what differential equations actually are and how to solve them, let's talk about the geometric intuition behind dynamical processes. To introduce key concepts, let's explore another fundamental model in biology. Now we're stepping into the world of coupled differential equations, where we will have multiple state variables and the rate of change of each depends on all the others. Consider the interactions between co-existing populations in a predator-prey model, often illustrated with rabbits and foxes. (11:40-12:10)

As the rabbit population grows, foxes have more food, leading to an increase in their numbers. However, more foxes means more rabbits get eaten, causing the rabbit population to decline. With fewer rabbits, the fox population shrinks, allowing rabbits to reproduce, and the cycle continues. (12:10-12:33)

**12:34 — 构建数学模型**

This intuitive understanding is certainly compelling, but can we build a simple mathematical model that would describe these oscillations? Let's start by defining our variables. x will denote the number of rabbits, and y will mean the number of foxes. (12:34-12:53)

**13:17 — 兔子的方程**

Rabbits reproduce at a rate proportional to their population, giving us the term ax, where a is the positive net growth rate. Rabbits also get eaten by foxes. We account for this with an interaction term minus b times xy. This term is proportional to the product of x and y, representing the probability of rabbits and foxes encountering each other. Thus, the prey equation: dx/dt = ax - bxy. (13:17-14:05)

**14:05 — 狐狸的方程**

Now for the predators. Foxes benefit from eating rabbits, converting a proportion of that energy into reproduction. We also include a term for natural deaths. This results in: dy/dt = cxy - dy. This simple model of two coupled differential equations is a very powerful tool for exploring the geometry of dynamical systems. (14:05-14:34)

**14:49 — 相空间 (Phase Space)**

Now, how do we solve this system? As before, we'll rely on numerical methods. However, to gain a deeper insight, let's visualize our data differently. Instead of plotting time as a horizontal axis and population size as the vertical, imagine a coordinate plane where x-axis represents the number of rabbits and y-axis represents the number of foxes. Notice that there is no time dimension here. Each point on this plane represents a possible state of our system at a given instant, with time governing the trajectory of switching between the states. (14:49-15:31)

Such a coordinate plane that corresponds to different states of the system as a whole is known as the phase space. (15:31-15:43)

**15:43 — 向量场与相图 (Vector Field & Phase Portrait)**

In this phase space, each point has two corresponding rates of change, the instantaneous velocities of the rabbit and fox populations. We can represent these as vectors, little arrows coming from each point. If we plot these vectors for many points, we create a vector field, showing how the system's evolution flows from any starting point. This is known as the phase portrait. With such visualization, we can gain qualitative insight into the system's behavior without doing precise number crunching. We can simply visually follow the arrows to get a feeling for the trajectory. (15:43-16:42)

**16:47 — 平衡点 (Equilibrium Points)**

With that model in hand, let's see what interesting dynamics we can observe. First, let's look for special points within our phase space where the system settles into balance. These are known as equilibrium points, and they correspond to both derivatives being equal to zero. If it falls into one of those states, it will remain there forever, as there is no mechanism for it to get out. (16:47-17:06)

Equilibrium points can be found by setting the right-hand side of our equations to zero, turning differential equations into a system of algebraic equations. Solving this gives us two equilibrium points: (0, 0) — both populations extinct, and another non-zero equilibrium — a balance between predators and prey. (17:09-17:42)

In our phase portraits, these equilibria appear as points where all arrows shrink to zero, indicating that once you reach that point, there is no way out. Rabbits and foxes will be exactly balancing each other out with no changes to the population dynamics. (17:45-18:02)

**18:06 — 原点(0,0)的稳定性**

Let's start with the origin. If we are slightly off of this point, let's say a few rabbits but no foxes, the population of rabbits will continue to grow exponentially, while the population of foxes remains zero. The (0, 0) equilibrium is unstable. The slightest perturbation sends the system away. (18:06-18:31)

If we have a few foxes but no rabbits, their population will go down, approaching extinction, as there is no food for the foxes to reproduce. (18:32-18:48)

**18:48 — 极限环 (Limit Cycle)**

Now, what about the non-zero equilibrium? If we start near that point and follow the arrows in our phase portrait, we see something remarkable. The populations cycle endlessly around the equilibrium, creating a closed loop. This behavior is called a limit cycle, and it will actually be fundamental when we talk about the excitability of neurons. (18:48-19:09)

Notice that we never explicitly put any oscillations into our system of equations. There are no trig functions or circles in the initial description. Limit cycles emerge from this seemingly simple dynamic law of interaction between the two variables. And there isn't just one — there are infinitely many cycling orbits. Which one you will end up on depends on the initial conditions. (19:12-19:37)

**19:37 — 参数变化的影响**

So far, we have fixed a particular set of parameters. Varying the values of a, b, c, and d doesn't fundamentally change the behavior of the system. It only affects the position of the non-zero equilibrium, as well as the exact shape and amplitude of the limit cycle oscillations. (19:37-19:54)

Slightly modifying our system of equations to account for the limited availability of food to rabbits leads to another interesting behavior. There is now a single stable equilibrium, which all trajectories converge to, defining the stable balance between rabbits and foxes. (19:54-20:18)

**20:18 — 总结与神经科学连接**

As we have seen, even such a simple system as the predator-prey model can exhibit very rich and complex behaviors. The idea of a phase portrait gives us a powerful visual tool to understand these dynamics without getting lost in mathematics. Ideas such as the stability of equilibrium points and the emergence of limit cycles form the foundation of dynamical systems theory, applicable to a variety of fields. (20:18-20:47)

Crucially, these same ideas can help us understand the intricate workings of the brain. Neurons, like the populations of rabbits and foxes, can be described as dynamical systems as well. The state variables might represent things like the membrane potential and the state of ion channels, instead of the population sizes. But all the underlying principles remain the same. (20:47-21:10)

However, to truly understand the differential equations that govern the dynamics of a neuron, we will first have to dive into the world of cellular biophysics, which deserves a dedicated video. So stay tuned for that next adventure. (21:10-21:24)

**21:24 — 赞助内容 (Brilliant.org)**

In the meantime, if you are interested to learn more about the mathematics we talked about today, you are going to love the message from our today's sponsor, Brilliant.org. Brilliant is one of the best places to learn math and physics online. They offer a wide range of interactive courses that make complex topics accessible and engaging. (21:24-21:45)

One course you might find particularly interesting is vector calculus. It is incredibly relevant to what we discussed today. Remember those portraits with arrows showing the directions of change? That's vector calculus in action. (21:52-22:07)

Ready to take your learning to the next level? Head to Brilliant.org/ArtemKirsanov to get a 30-day free trial of everything Brilliant has to offer, as well as a 20% discount on annual subscription. (22:32-22:47)

**22:47 — 结尾**

If you liked the video, press the like button, share it with your friends, and subscribe to the channel if you haven't already. Also, consider supporting me on Patreon, where you can find text versions of video scripts containing all the math details, as well as the ability to vote and suggest video topics. Stay tuned for more computational neuroscience and machine learning topics coming up. Goodbye and thank you for the interest in the brain. (22:47-23:10)