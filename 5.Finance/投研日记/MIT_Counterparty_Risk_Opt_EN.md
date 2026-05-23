---
title: MIT Lecture 10 - Counterparty Risk Optimization (English Transcript)
type: summary
created: 2026-05-23
source: https://www.youtube.com/watch?v=VbtXo62ROC4
tags: [finance, counterparty-risk, optimization, MIT, lecture]
---

# Lecture 10: Counterparty Risk Optimization

**Source:** MIT OpenCourseWare
**URL:** https://www.youtube.com/watch?v=VbtXo62ROC4
**Speaker:** James Shepherd (Quantile)
**Duration:** 1:21:23

## English Transcript (with timestamps)

[00:11] PROFESSOR: All right.
[00:11] Well, today's guest lecturer is
James Shepherd with Quantile--
[00:16] JAMES SHEPHERD: Quantile, yeah.
[00:18] PROFESSOR: --which is a wholly
owned subsidiary of LSEG.
[00:23] And your background in
quant finance is quite long.
[00:31] And so I'll let you share
some of the highlights.
[00:33] JAMES SHEPHERD: OK.
[00:34] PROFESSOR: Thank you
very much, James.
[00:35] JAMES SHEPHERD:
Thank you very much.
[00:36] Do I need that.
[00:36] PROFESSOR: No.
[00:37] JAMES SHEPHERD: OK.
[00:37] Thank you very much.
[00:38] Thank you for having me.
[00:40] This supposed to finish
about-- so a quarter to 4:00.
[00:42] Yeah.
[00:44] I'd like to leave some
time for questions.
[00:45] PROFESSOR: Until-- yeah.
[00:46] 10 to 4:00.
[00:47] JAMES SHEPHERD: OK.
[00:48] Thank you very
much for having me.
[00:50] Yes, I'm James.
[00:51] Yes, I work for
Quantile Technologies.
[00:54] That's a fintech company,
founded in about 2016,
[00:59] to do counterparty
risk optimization,
[01:02] which is the subject
of today's talk.
[01:05] A couple of years
ago, we got bought out
[01:07] by the London Stock
Exchange Group, which
[01:09] is why my email now says LSEG.
[01:12] Prior to that, I was at Morgan
Stanley for quite a long time,
[01:16] which is where I know
Vasiliy and Jake from,
[01:19] which is how I've ended up here.
[01:23] So we're going to
talk today, we're
[01:24] going to work our way up
to talking about optimizing
[01:29] a thing called initial
margin, which is
[01:31] a measure of counterparty risk.
[01:35] So we're going to
start off talking
[01:37] about different types of risk.
[01:39] Sorry.
[01:39] PROFESSOR: [INAUDIBLE]
[01:42] JAMES SHEPHERD: I've just
emailed them to Peter.
[01:45] Sorry about that.
[01:46] PROFESSOR: [INAUDIBLE]
[01:48] JAMES SHEPHERD: The
first view is just
[01:49] kind of like warmup stuff, so
you're not missing too much.
[01:53] So the first part of the talk,
we're going to talk about
[01:56] are different types
of risk that you
[01:58] have with derivative trading.
[02:00] And we're going to talk
about expected shortfall
[02:03] and value at risk.
[02:05] Just out of interest?
[02:06] Do people know what
these terms are,
[02:08] or is it worth my explaining
them a little bit?
[02:12] AUDIENCE: Explain.
[02:13] JAMES SHEPHERD:
OK, I will do that.
[02:16] Then we'll talk about how
that relates to initial margin
[02:19] and counterparty risk.
[02:20] And then we'll work
our way up to how
[02:24] we optimize this initial
margin within a network
[02:29] of financial institutions.
[02:32] And we'll talk a lot
about the challenges
[02:35] that you get in the real world.
[02:38] Because this is a maths
talk, I feel morally obliged
[02:41] to chuck some equations in
the thing from time to time.
[02:44] But largely, I'll skip over
that and talk a little bit
[02:47] about some of the intuition,
some of the toy models.
[02:50] And I've put a
bunch of references.
[02:52] When you get the
thing, there's a bunch
[02:54] of references at the end, which
has got some of the proper maths
[02:57] and proofs and
more detailed stuff
[02:59] behind it, if you're
interested in that.
[03:04] So in the shape of
derivatives, when
[03:06] we talk about the
different kinds of risks
[03:08] that can arise when you're
trading derivatives,
[03:11] market risk is probably
the most common one.
[03:13] So that's the value of the
derivative goes up and down
[03:16] as the market changes.
[03:19] Credit risk, again, is
reasonably well understood.
[03:25] It's the rise when you've got
exposure to a debtor defaulting.
[03:33] Operational risk is largely
when somebody screws up.
[03:37] It's probably actually
the hardest one
[03:39] to do any mathematical
modeling on operational risk
[03:42] because it's quite hard to model
people just messing up, which
[03:47] is really what that is.
[03:49] Liquidity risk is when you've
got a transaction, which
[03:53] is well, as the name
suggests, illiquid,
[03:58] which can happen when you've
got a very large position.
[04:00] So if you're trying to
sell a massive position
[04:02] in some particular stock,
you start selling that thing.
[04:05] And then because you
start selling it,
[04:06] that moves the market.
[04:08] And so you can't sell the
whole thing at the position
[04:10] that the market was
when you started.
[04:13] So liquidity risk happens it's
a kind of obscure instrument.
[04:17] And we'll come
back to it in this.
[04:19] It happens again if you've got
a very, very large position.
[04:23] And what we're mostly
going to talk about today
[04:26] is counterparty risk, which
is the exposure that you've
[04:30] got when you trade derivatives
to a counterparty defaulting.
[04:36] I think maybe a question
you might have here
[04:40] is, what's the difference
between counterparty risk
[04:43] and credit risk?
[04:45] So the example you can
have to differentiate
[04:47] this is, if I do a trade
with Goldman Sachs,
[04:51] let's say, a credit
derivative swap that
[04:53] has some JPMorgan corporate
bond as the underlying,
[04:57] then I have credit risk
with respect to JPMorgan.
[05:00] Because if JPMorgan defaults
on its corporate bond,
[05:04] then the value of my
derivative will change.
[05:07] And I have counterparty
risk to Goldman Sachs
[05:10] because, depending
on what happens
[05:12] to the value of that derivative,
Goldman Sachs may or may not
[05:15] pay me that amount of money.
[05:18] That's the difference
between those two.
[05:22] Make sense?
[05:26] So once you've got
a type of risk,
[05:28] once you've got some
risk, generally speaking,
[05:31] you want to mitigate
it, i.e., reduce either
[05:34] the probability of it
happening, or reduce
[05:36] the impact of that
risk happening, not
[05:38] just for counterparty risk,
for all kinds of risk.
[05:42] Hopefully, reasonably obvious
that people want to try and make
[05:45] the impact of once you've
identified the risk,
[05:49] make the impact of that smaller.
[05:51] So there's a bunch of different
ways that you can do that.
[05:54] We're largely going day--
to talk about the hedging,
[05:58] which means book some
trades to offset--
[06:00] book some new trades, which will
offset the risk that you've just
[06:03] discovered that you've got.
[06:05] And we'll talk about
collateralization,
[06:08] which is really paying margin
payments from the person you've
[06:13] got-- the person
you're exposed to,
[06:15] you would collect
a margin payment
[06:17] from them, which is kind of
like an insurance payment
[06:19] against them defaulting.
[06:20] And that's mostly what we're
going to talk about today.
[06:24] There are other
things you can do.
[06:27] And there's a thing called
central clearing counterparties,
[06:30] which I thought nobody
would have heard of.
[06:31] But apparently, someone's--
Andrew Gunstensen has already
[06:34] mentioned this a little bit.
[06:36] So I hope I might
skip over this slide
[06:38] because they are important in
the trading of derivatives.
[06:44] So I have a quick slide on CCPs.
[06:48] So normally, you
trade derivatives,
[06:50] and they're bilateral trades.
[06:52] So JPMorgan trades with
Goldman Sachs and so on.
[06:54] So we've got here,
you've got four parties.
[06:57] Say, A trades with
B. A trades with C.
[07:00] It's got a position
of 100 versus B. 125
[07:03] in the opposite
direction versus C.
[07:05] And what a central
clearing counterparty does,
[07:09] as the name kind of
suggests, is that it
[07:11] steps into the middle
of all these trades.
[07:14] And so instead of A
facing B and A facing C,
[07:18] A just faces the CCP.
[07:20] And so does B, and so
does C, and so does D.
[07:24] Just by doing that you
haven't really achieved much.
[07:26] You've just changed
your counterparty risk
[07:28] from being versus B and
C to versus the CCP.
[07:35] But once the thing
is in the CCP,
[07:38] you've got both the
125 and the 100.
[07:41] And you can net those
two positions together.
[07:43] And so you can net
that down and say,
[07:45] well, now, instead of
having 100 plus 125,
[07:48] I've only got 25 as my risk.
[07:51] And the same story
for all the others.
[07:53] So in the case of B, when we
had exactly equal and offsetting
[07:57] positions, B's ended up with
no counterparty risk at all.
[08:00] So B's in a very,
very happy situation.
[08:02] And everyone else is slightly
happier than they were before.
[08:06] There are other advantages
of CCPs, which I'm not really
[08:11] going to talk about too much.
[08:12] But the thing to know
is that some derivatives
[08:15] are mandated to clear at CCP.
[08:19] So interest rate swaps--
[08:20] pretty much if you have a
standard vanilla interest rate
[08:23] swap, you have to do this.
[08:25] You don't get a choice.
[08:27] But more exotic trades like,
say, an interest rate swap
[08:29] or something-- an
interest rate swaption,
[08:33] they are not eligible
to be cleared at a CCP.
[08:37] So some are.
[08:38] Some are not.
[08:38] So what you end up
with is a portfolio
[08:41] with some bilateral
trades versus a bunch
[08:43] of different counterparties
and some trades at the CCP.
[08:47] So almost everybody will end
up with a mixture of stuff.
[08:56] So now we're going to talk about
quantitative risk measures.
[09:01] So what you want from a risk
measure, or any general risk
[09:04] measure, it should
quantify somewhat
[09:07] the size of the total risk or
the size of the total impact.
[09:10] How much money could
you possibly lose?
[09:12] And it should also
quantify the probability
[09:16] of losing that amount.
[09:20] So there's two aspects to it--
the size and the probability.
[09:23] So in 1999, there's
a paper by Artzner--
[09:29] there's a reference
at the back--
[09:32] came up with these properties
of a risk function, which
[09:37] is nice properties, which
are known as a coherent risk
[09:42] function if it satisfies
those five properties.
[09:46] Mostly, they say things
like the function
[09:50] behaves kind of normally.
[09:52] We'll come back-- so the
important one is subadditivity.
[09:59] Anyone heard of
subadditivity as a thing?
[10:03] So basically, what that says
is if I have two portfolios
[10:07] X1 and X2, and I've got some
risk on X1 and some risk on X2,
[10:11] and then I bash those
two portfolios together,
[10:13] and now I've got a combined
portfolio, the risk
[10:16] on my combined portfolio,
according to my risk measure,
[10:19] ought to be less than or
equal to the sum of the risk
[10:23] on the two portfolios I
had in the first place,
[10:25] which seems kind of sensible.
[10:26] If I put some stuff
here and some stuff here
[10:29] and put it together,
it seems unlikely
[10:31] that I've manufactured some
risk out of doing this.
[10:34] But now conversely, it
seems highly plausible
[10:36] that there might be some
diversification of putting
[10:38] these two things together.
[10:40] And so my overall risk
might well be smaller.
[10:42] It seems a very plausible
and reasonable property
[10:45] to ask for from a risk measure.
[10:54] So we're going to talk about
two risk measures in particular,
[10:57] which are probably the two
most common ones for looking
[11:00] at a whole portfolio.
[11:01] One is Value at Risk,
which I probably
[11:04] will keep referring to
as VaR, and the other
[11:06] is expected shortfall.
[11:08] So value at risk is
this amount here.
[11:11] It says, if I've got--
[11:13] it says, what is the maximum--
[11:17] for a given confidence level,
what is the maximum amount
[11:21] that I can say that I will
lose more than that amount.
[11:26] So for example.
[11:30] can I be 99% certain that I
won't lose more than $10 million
[11:35] over, say, the next 10 days?
[11:38] So I have a confidence
level is called beta.
[11:41] There's a time horizon, which
we'll talk about in a sec.
[11:45] And the VaR is how
much money can I
[11:49] be 99% or beta percent
confident that I won't lose more
[11:54] than this amount?
[11:55] The expected shortfall
says, conditional that I've
[12:00] exceeded that amount of loss,
so given I'm in the 1% tail
[12:06] if beta is 99%, or the
5% tail if beta is 95%,
[12:10] if I'm in that tail, what
is my expected loss, given
[12:14] that I've exceeded VaR?
[12:17] So that's what
expected shortfall is.
[12:19] So hopefully, it's
indicated on here
[12:21] that this is the percentage.
[12:23] This dark area here
is 1 minus beta.
[12:26] So this is, say, 1% or minus 5%.
[12:29] The VaR is the biggest amount
before I get into the tail.
[12:35] And the expected shortfall is
the average value of that tail.
[12:41] Clearly, the expected shortfall
should be bigger than the VaR.
[12:44] Hopefully, that's obvious for
the same confidence level.
[12:51] So VaR was kind of popularized
by JPMorgan in about the 1990s,
[12:59] something like that.
[13:00] Expected shortfall
came around about 2000.
[13:03] And both of them
are heavily used
[13:04] by regulators and lots and lots
of counterparty risk measures
[13:08] today.
[13:11] VaR is probably the most
well-known one and most common.
[13:15] It's got a couple of problems.
[13:17] The first problem is if you have
these kind of weird fat tail
[13:22] probabilities.
[13:24] So you've got two probability
distributions, red and blue.
[13:28] The blue has this weird
fat tail bit over here.
[13:31] And we'll just say, well,
the area under the blue bit
[13:35] and the red bit is the same.
[13:36] So both these distributions
have the same VaR
[13:39] because the area up to here--
[13:42] assume there's a little
bit of blue here.
[13:44] The area up to here is the
same as the area under that.
[13:47] So both these distributions
have the same VaR.
[13:50] But clearly, the blue one
has a much bigger probability
[13:54] of doing some fairly
horrific loss.
[13:56] And also, hopefully
clearly, the blue one
[14:00] would have a much bigger
expected shortfall
[14:02] than the red one because
the average of the blue one
[14:04] is about here.
[14:05] The average of the
red one is about here.
[14:07] So VaR doesn't distinguish
between those two
[14:10] different cases.
[14:11] And you might say,
well, this is ridiculous
[14:13] because nobody's
going to have a-- in
[14:16] real life that kind
of distribution
[14:18] can't possibly exist.
[14:19] But that is not completely
ridiculous distribution.
[14:23] It's not totally
uncommon trading policy
[14:27] to sell a whole bunch
out of the money options.
[14:30] And if you sell a bunch out
of the money options, what
[14:32] most of the time going
to happen is you're
[14:34] going to take a small profit
from the sale of those options.
[14:37] And most of the time, they will
expire still out of the money.
[14:40] They won't get exercised, and
you're going to take a profit.
[14:42] But some of the time the
market will move enough.
[14:46] And if it moves enough,
they'll get exercised,
[14:49] and you're going to lose a
lot of money on those options.
[14:51] So that-- even
though I did contrive
[14:53] that for the purposes
of this lecture,
[14:55] that kind of distribution
is not as ridiculous
[14:58] as you might think.
[15:01] So that's the first problem.
[15:03] The second related problem
is that value at risk
[15:07] is not subadditive.
[15:09] So this, again, a little
bit of a contrived example
[15:14] to show that if you
take, say, the 95% VaR.
[15:18] I take two portfolios A
and B, with those kind
[15:21] of probability of happening.
[15:24] A and B by themselves,
the VaR, is zero
[15:27] because there's a 96% chance
I'm going to lose nothing.
[15:31] So 95% the VaR is
going to be zero.
[15:34] The expected shortfall
of those things is given.
[15:37] I'm in that last 5% tail.
[15:39] 1% of the 5, I'm going to
lose nothing and 4% of the 5,
[15:44] I'm going to lose 100.
[15:45] So I get to 80.
[15:46] And if you do the maths and
just add the two things up,
[15:49] and you do the A plus
B, you can discover
[15:51] that the VaR of the
combined portfolio is 100,
[15:53] and the expected
shortfall is 103.
[15:57] So that is a kind of
example that shows
[15:59] that VaR is not subadditive.
[16:03] Expected short--
obviously, this is not
[16:05] proving that expected
shortfall is subadditive.
[16:07] It is, in this case.
[16:09] It's quite hard-ish to prove
that expected shortfall is
[16:12] subadditive.
[16:13] It is.
[16:14] And I put one of the
things at the end
[16:17] is seven different proofs
that it is subadditive.
[16:19] So you can pick your favorite
one from the thing at the end.
[16:25] I also put an
example at the end--
[16:27] so even though this one is
a very contrived example.
[16:31] So in real life, most things are
kind of normal or normal-like.
[16:37] And in that case,
VaR is subadditive.
[16:41] So in real-life situations,
this is not as much of a problem
[16:45] as you might think.
[16:46] And there's a paper at the end.
[16:48] It talks also a lot
about that and says,
[16:51] actually, lots of
people criticize VaR
[16:53] because they come up with
these kind of crazy examples,
[16:55] but it's not too bad.
[16:57] For our purposes, given we want
to go on to optimizing stuff,
[17:03] it is critically bad.
[17:04] Because subadditivity--
we'll come back to this
[17:09] again in a sec-- is basically
the same thing as convexity.
[17:12] So not being subadditive
means VaR is not really
[17:16] a convex function, in general.
[17:18] And convex functions
are way, way, way easier
[17:21] to optimize than
nonconvex functions.
[17:24] So even though
it's not a problem
[17:27] if you just want to know VaR.
[17:28] It is a massive problem
if you want to optimize
[17:31] one of these things.
[17:33] And we'll come back to
this again in a little bit.
[17:39] I just wanted to
quickly point out
[17:41] that there's lots and lots
of other risk measures
[17:43] you can possibly choose here.
[17:45] VaR and expected
shortfall just happened
[17:47] to be the two common ones.
[17:49] You can characterize a risk
measure by how much weight
[17:53] it puts on a
particular percentile.
[17:55] So VaR is putting all of its
weight on the beta percentile.
[17:59] Expected shortfall
puts zero on everything
[18:00] less than beta and averages
out everything above beta.
[18:04] But you could say,
well, both of those--
[18:06] you can make some
criticisms of them.
[18:09] You could say, well, I should
put a little bit of weight
[18:11] on something that's a bit
less than the beta percentage,
[18:14] and I should weight the--
[18:15] the really, really
extreme tail losses,
[18:18] I should weight them more than
the just beyond the tail losses.
[18:22] So you can imagine having
these exponential spectral risk
[18:26] functions that have these kind
of functions, which do exactly
[18:29] those things, that they
put an awful lot of weight
[18:32] on the really bad losses at
the 99% and 99.9% things.
[18:38] And it scales off going down.
[18:41] It's just to point out there's
a few different choices
[18:45] you can make here.
[18:51] So both VaR and expected
shortfall, they've
[18:53] basically got two parameters.
[18:55] They've got the
confidence level,
[18:56] and they've got
the time horizon.
[18:59] So we'll talk a bit
about the time horizon.
[19:05] So that means I
want to make sure
[19:08] that I'm going to lose
less than this amount
[19:10] of money over one day,
five days, 10 days.
[19:13] That's the time horizon.
[19:15] How long have I got to avoid
losing this amount of money?
[19:18] If you were to
make the assumption
[19:20] that the change in the
portfolio-- so this delta
[19:25] P is a normal distribution,
then VaR and expected shortfall
[19:29] would have these
two formats here.
[19:32] So they would also be normal.
[19:37] And if you assume that people
make these kind of assumptions
[19:41] in the thing, that the mean
change on a daily basis
[19:47] is zero, which is not a
crazy kind of assumption,
[19:51] then both VaR and
expected shortfall
[19:53] would be proportional to
the standard deviation
[19:56] with these things.
[19:57] They would be normal.
[19:58] And if you did that,
and you assumed
[20:01] that all the daily changes
were independently--
[20:05] they were all kind of
independent identical normal
[20:08] distributions so you
could add them all up.
[20:09] Then you would
discover that the T-day
[20:11] VaR and the T-day
expected shortfall
[20:13] is proportional to the square
root of the one-day VaR, which
[20:17] is the normal approximation that
people make with those things.
[20:22] In reality, it seems
that the losses--
[20:28] the changes that you'd
have on a typical portfolio
[20:30] or a typical market data
are not independent.
[20:33] If you lose a lot
of money one day,
[20:35] it's a reasonable
chance you might
[20:36] lose some money on the--
or the market might go down
[20:38] on the second day.
[20:39] So there's a thing
called autocorrelation,
[20:42] which is basically the
correlation of a time series
[20:44] with itself shifted by one day.
[20:46] And so you can-- which
is what this thing here.
[20:51] And if you assume that that
autocorrelation, rho, is
[20:54] some number, then it
would modify the T-day VaR
[21:01] for two days by this formula.
[21:03] So I put in this table.
[21:05] So the top row is assuming that
there's no autocorrelation.
[21:09] So that's 1 root 2 root 5, root
10 and so on is the top row.
[21:13] And then as you increase
the autocorrelation,
[21:16] the T-day VaR, as a
function of the one-day VaR,
[21:21] gets bigger and bigger.
[21:23] So I did some--
[21:24] I'll show you some
market data in a sec.
[21:25] So I took a set of observations
from the EURO-STOXX stock index.
[21:30] And that suggests that the
rho, the autocorrelation,
[21:35] is about 0.1.
[21:36] I did some other
indices, and they
[21:38] were all between 0.05 and 1.15.
[21:42] So 0.1 is kind of reasonable.
[21:45] And generally, people take a
10-day VaR thing as a normal
[21:51] thing.
[21:52] So you'd be looking at about
this number here, this 3.46.
[21:59] It's about-- that means to say
that the standard approximation
[22:03] of using the square root of--
[22:07] saying the square root
of the one-day VAR--
[22:10] sorry-- the square root
of T times the one-day VAR
[22:13] is probably going to
underestimate the actual T-day
[22:16] VaR by about 10% because
it's 3.46 divided by 3.16.
[22:22] But nevertheless,
almost everybody
[22:26] just says that the T-day VaR is
the one-day VaR times root T.
[22:32] So this is where I
got the data from.
[22:35] So I picked four stock indexes--
[22:39] Ibex, CAC, DAX, and EURO-STOXX.
[22:42] That's, if you don't know,
Spanish, French, German,
[22:45] and a kind of
pan-European stock index.
[22:50] So from 2006 to
2024, you can see
[22:53] there's a couple of
periods of stress in here.
[22:56] One in 2008 time frame,
around about here,
[23:01] which was the global
financial crash,
[23:03] and one in about
2020, which was COVID.
[23:07] And some degree of calmness
in between those two periods.
[23:12] Clearly, there's some
correlation between these things
[23:18] that's there.
[23:20] On a practical note,
there's a couple
[23:21] of things worth pointing out.
[23:22] I picked these stock indices
because they're all European,
[23:26] which means I don't need
to worry about FX rates
[23:29] when I'm playing
with these things.
[23:32] But even though
they're European,
[23:34] they're from
different countries.
[23:35] And the different countries
have different holidays.
[23:40] And so you have
to decide what I'm
[23:41] going to do-- what you're going
to do when one of these indexes
[23:44] is on holiday and not trading.
[23:48] What I did here was that if
all of them were on holiday,
[23:50] I'm ignoring the day completely.
[23:52] And if one of them was not on
holiday, but the rest were,
[23:55] I just fill forward.
[23:56] And so you'd see a daily
change of zero on those.
[23:59] That might not necessarily be
the most sensible thing to do.
[24:02] It doesn't really make
that much difference.
[24:04] But the reason I mention
it is because if you
[24:08] work in this kind of
industry for that,
[24:11] you end up spending a surprising
and disproportionate amount
[24:15] of time dealing with both
FX and holiday calendars.
[24:19] You probably don't
expect to be doing this.
[24:21] But holiday
calendars-- you spend
[24:24] a lot of your time
trying to work out
[24:26] what are you going to do
with these kind of things?
[24:32] So there's a couple of different
ways you can estimate VaR.
[24:35] One is historical simulation,
and one is doing model building.
[24:42] We'll have a quick
look at both of them.
[24:45] So the historical
simulation, basically
[24:47] is we're going to go back
and look at the time series.
[24:50] We'll look at the value of each
of these indices, the CAC, DAX,
[24:54] IBEX, and EURO-STOXX
on each day.
[24:58] And we'll come up
with a portfolio.
[25:00] So I just made up
some portfolios.
[25:01] Say I'm going to have 3,000
units of CAC, 4,000 of DAX,
[25:04] and so on and so on.
[25:06] And we'll call that
the portfolio weight.
[25:08] And so now, I can figure
out that on the day--
[25:13] the change in value
on day I is going
[25:17] to be the relative change in
the underlying market index.
[25:21] For example, the second
row minus the first row
[25:24] for the first day
and so on, multiplied
[25:25] by the weight for that index.
[25:28] Then just sum it up
over all the indices.
[25:30] And that will give me the
change on the I-th day.
[25:38] So then I can take the
distribution of those things,
[25:41] and I will get something
that looks like that.
[25:45] Hopefully, that's big enough.
[25:48] So one thing to add
here is that when
[25:50] you're doing that,
when you're looking
[25:51] at these historical
simulations, you
[25:55] have to decide over what period,
over what historical period,
[25:59] am I going to look at?
[26:01] And the main thing
to notice here
[26:03] is that depending on what
historical period you look at,
[26:07] it makes a massive difference
to both the VaR and the expected
[26:10] shortfall.
[26:12] So what normally happens, if
you normally talk about VaR,
[26:15] you talk about the most
recent, say, two years.
[26:20] These are all two-year
periods, by the way.
[26:22] So the top left, 2022
to the end of 2023.
[26:25] Given my series went
up to the end of 2023,
[26:28] this top left box would
be what you would normally
[26:31] put in as VaR, the most
recent 500 days, basically,
[26:35] assuming there's 250
days in a year, which
[26:37] is more or less true.
[26:39] The ones on the right, they're
from the two stress periods--
[26:43] the global financial
crisis and COVID.
[26:46] And as you might imagine, if you
compute VaR based off those two
[26:52] periods, you get a
much, much bigger number
[26:54] than you do of either of
the calm periods, the most
[26:57] recent one, 2022, or
a period in between
[27:00] the global financial crisis and
COVID, 2015 to 2016 with that.
[27:07] So that makes, by far and
away, the biggest difference,
[27:10] which period you choose.
[27:12] And because of that, regulators
have recently introduced-- well,
[27:17] not that recently-- introduced
the concept of a thing
[27:19] called stress VaR.
[27:20] So in addition to taking
the most recent two years,
[27:23] five years, 10 years,
whatever you decide to choose,
[27:26] you also pick a fixed period
known to be stressful.
[27:31] So people will
pick either COVID,
[27:33] or they will pick the
global financial crisis.
[27:36] And then that's
generally known as S-VaR,
[27:38] or stressed VaR because
there's such a big variation
[27:42] in these terms that are there.
[27:47] And then just to break it down
in terms of what you actually
[27:52] did here, what I actually did
was I took all those changes--
[27:55] so there was 500 changes in
each period, more or less.
[27:58] I ordered them from
the biggest change
[28:00] to the-- from the biggest
loss to the biggest gain,
[28:03] these things here.
[28:04] And then the 5th worst one--
that's the VaR, for the 99% VaR,
[28:10] because that's 1%.
[28:11] And the 12th worst
one, that's the 97.5.
[28:14] It's not that complicated.
[28:16] You just order the thing.
[28:17] You take the 5th worst one, 12th
worst one, that's what VaR is.
[28:19] And expected
shortfall, for the 99%,
[28:23] you take the average
of the worst four.
[28:26] And for the 97.5, you take
the average of the worst 11.
[28:31] There is some debate about that.
[28:34] Some people claim you should
take the average of the worst
[28:36] five, so including the 320, and
the average of the worst 12.
[28:40] I think standard market
convention is to take the four.
[28:44] Doesn't matter that much.
[28:46] But that's all that's actually
happening here to do these.
[28:54] All OK so far?
[28:57] To do the model building
approach, it's kind of similar.
[29:02] We just make the assumptions
that everything is normally
[29:04] distributed.
[29:06] The daily changes are
normally distributed
[29:07] with mean zero and
a sigma I. We assume
[29:13] that there's some kind of
correlation between all
[29:15] the different indices.
[29:16] And
[29:16] So you say, well, the
sigma for the portfolio
[29:18] is going to be this term here.
[29:22] So there's a variance-covariance
matrix between the-- right--
[29:27] that you get.
[29:29] And using the assumption that
VaR and expected shortfall
[29:32] are proportional
to the sigma again,
[29:36] you get these two expressions.
[29:39] So all you need to do for the
model-building approach is
[29:41] figure out what the
variance-covariance matrix is
[29:44] between these different
elements, which I computed here.
[29:48] And I come up with a VaR,
and I get these two numbers--
[29:52] 225 and 257.
[29:55] The main thing to
note about that
[29:57] is that it's significantly,
significantly less
[30:00] than the historical VaR.
[30:03] So the 99th-- this is computed
for the 2022-2023 period.
[30:07] So the historical VaR--
[30:12] those equivalent numbers
were 320 and 377,
[30:15] basically showing that
these normal distributions,
[30:20] it's clearly not a
normal distribution.
[30:22] There's a fatter tail in
there than you would expect.
[30:25] But you can say, well--
[30:28] you can work out, is this
an acceptable VaR model?
[30:31] Yes or no.
[30:32] So what you can say is
given I've got something
[30:36] where I'm going to take 500
trials, and I expect to see--
[30:41] and I expect the
VaR-- the actual loss
[30:44] to have exceeded the VaR
1% of the time, that's
[30:47] the definition of VaR.
[30:49] And what is the probability that
I'm going to see 12 or more--
[30:55] so there's 12
violations, by the way.
[30:57] So if I take this 225 and say,
how many times did it actually--
[31:03] according to that period,
how many times was it
[31:05] actually-- the loss
was bigger than 225,
[31:08] or there were 12
scenarios bigger than 225?
[31:11] So what is the
probability that I
[31:14] would see 12 or more days
out of a sample of 500 that
[31:18] exceeded the VaR?
[31:22] So that comes from the
binomial distribution, which is
[31:26] that formula, and you get 5.2%.
[31:29] And the general rule of thumb
is that if the probability is
[31:33] 5% or more of getting that
degree of-- that number
[31:37] of violations of the VaR,
you say that the model is OK.
[31:42] And if the probability
is less than 5%,
[31:46] you'd probably reject
the model and say
[31:47] the VaR is not a good model.
[31:49] So even though the VAR
here is significantly lower
[31:53] than the historical
simulation, you
[31:56] would probably accept that
as an OK kind of model.
[32:02] And the only other point
I wanted to make on that
[32:08] is that what we've
basically done
[32:10] there is a back-testing of VaR.
[32:12] So we basically came up
with a model, and we said,
[32:14] how good is that model?
[32:15] How many times, based on
some historical simulation,
[32:19] was the VaR exceeded?
[32:23] So it's really, really easy
to do back-testing of VAR.
[32:27] The single main reason
why people still
[32:31] use VaR over
expected shortfall is
[32:34] because doing this for expected
shortfall is quite tricky.
[32:38] It's not even
clear what it means
[32:40] to do back-testing of
expected shortfall.
[32:42] Because, I mean, the
expected shortfall
[32:46] is a function of the
probability distribution.
[32:50] It's the mean of the tail.
[32:51] You can't really compare
that with one sample
[32:54] that I've drawn from
the distribution.
[32:56] It's like comparing
apples with oranges.
[32:59] There's a whole bunch
of debate around
[33:02] whether back-testing expected
shortfall is flat-out
[33:06] impossible, difficult, or not.
[33:09] And there's a bunch of papers
at the end on this as well.
[33:14] But it's definitely a lot
trickier than doing it for VaR.
[33:18] And that is the main
reason, people still
[33:20] use VaR, despite
its shortcomings
[33:22] around the subadditivity and
the handling of the tails.
[33:27] So I'm going to skip
over some stuff.
[33:29] This is some stuff
around regulation.
[33:33] And I'll just quickly
mention this slide because--
[33:38] so one of the problems
with expected shortfall
[33:41] is it's kind of defined
in terms of VaR,
[33:46] because it's the mean
loss that you would get,
[33:49] given you've exceeded
VaR in the first place.
[33:52] What you can do is there's a--
[33:55] this function here--
this is in the paper
[33:57] by Rockafellar and Uryasev,
which is in the back.
[34:01] It says, if you take
this function F, which
[34:03] is this expression here,
and you try-- and then
[34:08] you minimize that over alpha.
[34:09] You consider this to be
a function of X, which
[34:11] is the portfolio, and
alpha is just a number,
[34:16] and you minimize
this over alpha,
[34:18] then the minimal
value of that function
[34:21] is the expected shortfall.
[34:23] And so you can find the expected
shortfall by taking that F
[34:27] and minimizing it.
[34:28] And that is basically if
you replace the integral
[34:31] with a sum, that's
basically a linear problem.
[34:35] And so it's relatively easy to
find the expected shortfall.
[34:39] Moreover, if you minimize it
with respect to alpha and X,
[34:44] now what you've
done is you've found
[34:46] the portfolio with the minimal
expected shortfall, i.e.,
[34:51] you have minimized the
expected shortfall,
[34:54] which is basically
what we're trying
[34:55] to do in this whole thing.
[34:59] So you just have to
consider this function here.
[35:01] You can minimize that
over X and alpha,
[35:04] which is basically
a linear problem.
[35:06] And that essentially is how you
minimize expected shortfall.
[35:11] No such equivalent thing
exists for value at risk.
[35:15] So even though expected
shortfall is trickier
[35:18] to back test, it's
easier to minimize,
[35:26] which is what I care about
more I'll skip over it.
[35:33] So that's expected
shortfall and VaR.
[35:36] So now we're going to start
talking about counterparty risk
[35:38] and margin.
[35:41] So if you have in the
derivative world--
[35:47] so if I have A has
got two trades,
[35:49] one with B, one with C.
Derivatives typically swaps,
[35:53] means I'm going to
exchange a series of cash
[35:55] flows between the two parties.
[35:58] And typically, those
cash flows will
[35:59] be exchanged, say, over
a three-month period
[36:01] or six-month period.
[36:03] So A, in this case, is
receiving some cash flows.
[36:07] It's paying the series
Si to B and receiving Ti
[36:10] from B. A is exposed to the
fact that before the next cash
[36:15] flow arrives from B, B
might default and not pay
[36:19] the cash flow.
[36:20] And the same story for C.
[36:22] So A has counterparty
risk to both B and C
[36:26] because when we get to the next
cash flow date in, say, three
[36:29] months time or six months
time or a year's time,
[36:31] they might not pay that
cash flow that they're due.
[36:34] So that's the
fundamental reason why
[36:36] they have counterparty
risk for derivatives.
[36:38] In order to mitigate
against the fact
[36:41] that there might not
pay that cash flow,
[36:44] what actually happens
is that they pay--
[36:46] is that all these counterparties
exchange on a daily basis
[36:50] the exchange variation
margin, which
[36:56] means that-- which is equal to
the value of these derivatives.
[36:59] So as the value goes up
and down of these things,
[37:02] they'll be paying variation
margin to one another.
[37:05] And that mitigates against
the cost of the cash flow
[37:08] not getting paid.
[37:09] But if they're paying variation
margin from one to another,
[37:11] and then one party or other
goes bust and defaults,
[37:16] then you've still got
to pay the variation
[37:18] margin to the other person.
[37:20] And as soon as one party goes
bust, what A would try and do--
[37:23] so if C goes bust here, A would
try and replace that trade.
[37:26] It would take it
some number of days
[37:28] to replace that trade
with something else
[37:30] or unwind that trade,
during which time
[37:33] the value of that
trade might go up.
[37:35] And because the value of
that trade is going up,
[37:37] it's having to pay an increased
amount of variation margin to B.
[37:42] And so therefore,
it incurs a loss.
[37:44] And so it incurs a loss because
during the period between when
[37:48] C defaults and when it
manages to replace that trade,
[37:51] the value of the trade will
change or go up, basically.
[37:57] And that is the loss.
[38:00] So in order to mitigate
against that risk,
[38:03] A will collect initial margin.
[38:06] That's what initial margin is.
[38:08] That's essentially
a covering you
[38:09] for the risk in between
when a party defaults
[38:14] and when you manage to unwind
or replace that position.
[38:19] That slide just says
what I just said.
[38:23] And then I have another slide,
which says the same thing again
[38:25] in a picture.
[38:26] So you have the variation margin
is getting paid up until here
[38:32] between all these things.
[38:34] You get some default
will happen here.
[38:36] We don't know what's
going to happen.
[38:37] The risk can go up or down.
[38:39] And some loss could potentially
be incurred at this point.
[38:44] This should hopefully
sound to you
[38:46] a little bit like what we just
discussed with VaR and expected
[38:49] shortfall.
[38:50] And so initial margin--
[38:51] in order-- how much initial
margin should I collect?
[38:54] Well, basically it's going to
be a VaR based on how long you
[38:58] think it's going to take you
to unwind that position, which
[39:01] is called the margin
period of risk.
[39:05] There's two kinds
of initial margin,
[39:07] depending on whether your
trade is a cleared trade
[39:10] or a bilateral trade.
[39:13] The cleared margin is set up
by the clearing house, the CCP.
[39:19] And that's always been the case
for years and years and years.
[39:22] Up until 2016, people were
not paying initial margin
[39:26] on bilateral trades.
[39:28] That changed when ISDA came
up with their standard initial
[39:31] margin, which is the form--
[39:35] I've put the formula down here,
but it's kind of similar--
[39:37] it's basically VaR is
what they put here.
[39:41] And the only difference compared
to what we just discussed
[39:44] is that because it's handling
nonlinear portfolios,
[39:48] there's a gamma
term in there, which
[39:51] I didn't talk about before.
[39:53] And when you work it
all the way through,
[39:55] you make exactly the
same assumptions,
[39:57] that everything is normal.
[39:58] Mean is zero.
[40:00] You end up with the exact
same term we saw before.
[40:04] Or you also--
[40:05] SIMM assumes that it's a
10-day margin period of risk.
[40:09] And it's a 99%
confidence interval.
[40:11] So the 99% confidence interval,
that's the inverse normal of 99%
[40:17] That's the 10-day
margin period of risk.
[40:23] That's the exact same term we
looked at in the VaR before.
[40:26] And then you get
two additional terms
[40:28] that come from the convexity,
which is kind of similar.
[40:32] The main point is that
initial margin is basically
[40:37] some variant of VaR, or
potentially expected shortfall.
[40:43] In real life, there's lots
and lots more simplifying
[40:46] assumptions that people
make around all these things
[40:52] to try and simplify stuff.
[40:55] And all these kind
of correlations
[40:57] between all the different
parameters-- this
[40:59] covers the entire world,
all different asset classes,
[41:04] by the way.
[41:04] And so they get kind of
recalibrated on a yearly basis.
[41:08] If you Google SIMM
COVID now, you'll
[41:13] probably see quite
a lot of stuff
[41:15] in there because SIMM
2.7 is about to come out
[41:19] in the beginning of December.
[41:21] And that'll be the
first one that's
[41:22] calibrated without any of the
COVID or global financial crisis
[41:28] data in there.
[41:29] And what's going to happen,
what people expect to happen,
[41:32] is that the initial margin
calculated by this SIMM
[41:34] is going to massively
reduce by somewhere
[41:36] in the region of 5% to 20%.
[41:39] And what that will do
is release something
[41:42] in the region of $40 billion of
margin back out into the wild.
[41:46] Because today, people are
paying initial margin,
[41:48] all these different things
with these high levels of--
[41:50] using these high levels of VaR.
[41:52] When they recalibrate in
the first week of December,
[41:55] everything will come down.
[41:56] Everybody will release
all the initial margin.
[41:59] So there's quite a lot
of stuff around that
[42:01] in the news at the moment.
[42:04] That just talks about
how the structure--
[42:06] you roll everything up
into one number across all
[42:09] the different portfolios.
[42:13] And I'll skip over that.
[42:16] So that's what margin is.
[42:18] So now we come on to trying to
optimize the initial margin.
[42:24] I put margin here.
[42:24] I mean initial margin.
[42:27] So the situation that
we're thinking about
[42:30] is we've got multiple different
financial participants--
[42:32] A, B, C, D, E. Think
of them as banks.
[42:34] And we've got--
[42:36] I've put one CCP.
[42:38] There could, in fact, be
multiple CCPs in the middle.
[42:41] And all these
participants have got
[42:43] a bunch of bilateral
trades versus each other,
[42:45] and they've got a bunch
of trades versus the CCP.
[42:50] That's the situation
that we've got.
[42:52] And they're all posting margin
to each other in this situation.
[42:58] And what we are trying
to do by optimizing stuff
[43:03] is come up with a bunch
of hedge trades, which
[43:07] is these X, H variables between
all the different participants
[43:11] in order to try and
minimize the margin, i.e.,
[43:15] the VaR, in the entire system.
[43:17] That's the goal of what
we're trying to get to.
[43:22] And you might say, well, why are
there no trades versus the CCP?
[43:26] Well, you're ignoring
the cleared margin.
[43:29] That's just a practical issue.
[43:31] You can't book trades
between the CCP and a bank.
[43:37] All you can do is book
bilateral trade between A
[43:40] and B, A and E, all
these different things.
[43:42] And depending on which trades
you choose, some of them
[43:47] will be cleared or not cleared.
[43:48] If you pick a trade, where the
trade type is like an interest
[43:52] rate swap, then that will
be mandated to clear.
[43:55] And so even though it's between
A and B, it'll get cleared.
[43:58] And it will affect the
cleared margin and not
[44:00] the bilateral margin That's why
there's no actual trades booked
[44:05] between the CCP and
any of these people,
[44:08] Because that's what
we're trying to do.
[44:11] So that's the problem
we're trying to solve,
[44:14] which looks like a lot
of maths, but in fact,
[44:17] is not that complicated.
[44:19] So what we're trying
to do, is we're
[44:21] trying to minimize summed over
all of the parties, so all
[44:24] of the banks--
[44:25] A, B, C, D, E--
[44:27] the margin of all those people.
[44:29] So the margin is
made up of the SIMM,
[44:33] the bilateral margin summed
over all the counterparties,
[44:37] plus the cleared margin
summed over all the CCPs
[44:41] that are there.
[44:42] So that just says the sum of
all the margin in the system
[44:45] is what I'm trying to minimize.
[44:47] And we say, well, where SIMM
and the initial margin, there's
[44:50] some functions of risk,
as we've discussed.
[44:53] We know what the function is.
[44:54] It's Var-like, let's say.
[44:57] So we know that SIMM and--
[44:59] oops, sorry-- initial margin
are some functions of the risk.
[45:04] And we know that the risk
position that's there
[45:08] is equal to the
initial risk, which
[45:12] is the zero, plus the
sum over all the hedges
[45:16] that we're going to book.
[45:17] So we're going to propose
a bunch of trades.
[45:19] So we sum over all
the hedges that we're
[45:21] going to book, the
size of the hedge which
[45:23] is the X, which is the
thing we're trying to find,
[45:26] multiplied by the risk
of that particular hedge.
[45:30] So that's how we know
what the new risk is.
[45:33] And we've got a
couple of constraints
[45:35] that we need to
put in the system.
[45:38] This is the most important one.
[45:39] This is what we call
the symmetry constraint,
[45:42] even though it
looks like it looks
[45:44] like an asymmetry constraint.
[45:46] What this says is that if
P sells something to Q,
[45:51] Q had better buy that same
thing from P. Exactly.
[45:56] And this was-- when
we first set this up,
[45:59] this was, in reality, the thing
that people were most worried
[46:02] that we would mess up.
[46:03] Because the biggest problem
that could have happened here
[46:06] is that we told--
[46:07] we set up a thing.
[46:09] We tell a Goldman Sachs, go
and buy 100 million of stuff
[46:13] from JPMorgan.
[46:15] And then we tell JPMorgan,
go and sell 200 million
[46:19] of stuff to Goldman Sachs.
[46:21] So Goldman Sachs sees their
thing, and says buy 100 million.
[46:24] They think, that
looks good to us.
[46:25] We'll agree to this.
[46:27] JPMorgan sees their thing, which
says, sell 200 million of stuff
[46:30] to Goldman Sachs.
[46:31] And JPMorgan goes,
that looks good.
[46:33] We'll agree to this.
[46:35] Goldman Sachs doesn't see
what we told JPMorgan,
[46:37] and JPMorgan doesn't see
what we told Goldman Sachs.
[46:40] And they only discover
that something's
[46:42] gone horrifically wrong when
they try and do that trade.
[46:47] So the reason that
doesn't happen
[46:49] is because we've got this
constraint in the system that
[46:52] says that, whatever Goldman
Sachs buys from JPMorgan,
[46:54] JPMorgan had better sell that
exact same thing to Goldman
[46:57] Sachs.
[46:59] That is the most important
constraint in the whole system.
[47:02] The second constraint, the big
one that we've got in there,
[47:05] is this one, which says--
[47:07] this is cash flow flatness.
[47:09] This says that for
any party, let's say,
[47:12] Goldman Sachs, if I sell
something to one party,
[47:19] I'd better buy that
exact same thing
[47:21] from some combination
of other people.
[47:24] That's what that
constraint says.
[47:26] We don't need that
to be in the system.
[47:29] It's a kind of safety
valve that's in there.
[47:33] The advantage of
having this in here
[47:34] is it says, if I'm definitely
sure that everything
[47:37] is cash flow flat
across the system,
[47:40] nobody's going to make any
money or lose any money out
[47:43] of the whole system.
[47:44] Because I'm going
to sell something.
[47:46] I'm going to sell
something to there.
[47:47] I'm going to buy it
from somewhere else.
[47:49] So I'm just-- all I'm
doing is shuffling risk
[47:51] around the system.
[47:52] You could relax that,
and you could say, well,
[47:56] some parties could
make some money.
[47:57] Some could lose some money.
[47:58] Some could change some risk.
[48:00] But it makes everything
a lot trickier.
[48:02] So we basically enforce
this around the system.
[48:06] And then the last constraint
is a risk constraint
[48:09] which comes from the
parties themselves.
[48:12] And what this says is that
Goldman Sachs or some party
[48:16] might say, well, I don't
really want to go--
[48:19] I might not want to go
long a particular risk
[48:22] factor versus some particular
counterparty for whatever
[48:25] reason.
[48:27] So the first two are
system-wide constraints
[48:30] that we impose on the thing.
[48:32] And the last one is a
constraint which basically
[48:35] says, don't change the risk too
much, which is what parties say.
[48:40] So all of that maths,
that's all it's saying.
[48:46] So if we look at-- it's
kind of-- if we look
[48:48] at a very, very simple example.
[48:50] If I take a three-party system--
[48:52] A, B, C-- so this
might be a bit small--
[48:55] and you put it in
there and say, well,
[48:57] how could I minimize the
margin around that system?
[48:59] And the way you'd
minimize it, you've
[49:01] got AC's got to trade with
10, AB's got to trade with 2,
[49:04] and BC has got a trade with 9.
[49:07] Well, what you do is you
move the median trade
[49:09] around the whole triangle.
[49:12] If you move one median
trade around-- one trade
[49:14] around the whole
triangle, I'm guaranteed
[49:17] to satisfy by construction
those first two
[49:21] constraints because I'm only
moving the exact same thing
[49:24] around the whole system.
[49:26] And if I'm moving, just
say in this case, 9.
[49:30] I'm going to--
[49:31] A is going to buy 9, sell 9.
[49:32] B is going to buy 9, sell 9.
[49:34] C is going to buy 9, sell 9.
[49:35] So I'm going to satisfy the
second constraint as well.
[49:38] I've ignored the third
constraint for now.
[49:40] And the reason I
picked that is--
[49:42] those particular examples
with 2, 9, and 10,
[49:44] is that actually if you fiddle
around with the maths a bit,
[49:48] the thing you should move is the
median trade given any triangle.
[49:53] And you can take any
network, and you can always
[49:55] break a network into
a bunch of triangles.
[49:57] And for every triangle, you
just move the median around.
[50:00] That's what you should do.
[50:02] The problems are this won't
satisfy all the different--
[50:05] if you have additional
constraints, it causes problems.
[50:07] And obviously, some
edges of this triangle
[50:11] would also be edges
of other triangles.
[50:13] And so you end up and you
can-- it won't generally
[50:15] solve the problem.
[50:17] But it's a good way
of thinking about it.
[50:20] We always think about
triangles and how
[50:22] you would move risk around
in a particular triangle.
[50:28] So that's that.
[50:31] In reality, we just use a big
numerical solver around this.
[50:35] What we're in the
business here is
[50:36] we're solving minimization
problems or operational research
[50:41] type problems.
[50:42] They're of the form minimize
F subject to some other stuff.
[50:46] And as I mentioned earlier,
solving complex problems
[50:51] is way, way, way easier than
solving general, nonlinear
[50:53] problems.
[50:54] And convexity is basically the
same thing as subadditivity.
[50:57] That's the definition
of convexity.
[50:59] And that should remind
you of the definition
[51:02] we saw earlier of subadditivity.
[51:04] So we saw earlier minimizing
expected shortfall.
[51:07] That's basically a
piecewise linear problem.
[51:09] All these things we're talking
about, SIMM is nearly convex.
[51:13] There are different
add-ons that you can have,
[51:15] which are usually convex.
[51:17] And some of the maths
that we get into
[51:19] is, how do you come up with
approximations of these things
[51:23] which genuinely are convex.
[51:25] We tried using proper nonlinear
solvers on these things.
[51:28] Way easier just to approximate
the function you want and use
[51:31] a convex solver on it.
[51:33] Because the state of the
technology for solving convex
[51:35] optimization problems is
really, really, really good.
[51:39] It would be crazy to write
your own version of a convex
[51:42] optimization solver because
there are loads of open source
[51:45] and commercial available--
[51:47] things available.
[51:49] So don't do it.
[51:50] Just plug it into a
system, and it works.
[51:54] The thing to note is
that how difficult
[51:57] it is to solve the problem is
really, really, really sensitive
[52:01] on the specifics of the problem.
[52:02] And that doesn't really mean
the size of the problem.
[52:05] The size is not really
too much of an issue.
[52:08] It's all kinds of the
structure of the problem, how
[52:10] sparse is the problem.
[52:11] And the thing these
are the things
[52:13] that matter in the real world
[52:18] Also, it's a good idea to
use modeling languages.
[52:21] So there are lots of
modeling languages available.
[52:24] Gurobi is the one we use.
[52:26] I think you may-- people
might have used it.
[52:28] I think you can get
it for free if you're
[52:29] an academic institution.
[52:33] In case anybody wants to
spend 10 seconds trying
[52:35] to solve that in their head,
this is an integer problem,
[52:39] trying to minimize 5 x1 plus
8 x2 subject to those two
[52:42] constraints, you can probably
do that in your head.
[52:49] Hang on.
[52:51] So we did that.
[52:52] Sorry.
[52:56] So we did it on Gurobi.
[52:58] Using the 24 physical
cores probably
[53:02] is overkill for that
problem, but it comes up
[53:05] in 10 milliseconds
with the answer of 31.
[53:07] Hopefully, if you
did it, that's what
[53:09] you tried, just to show
how easy it is to solve
[53:14] some of these problems.
[53:16] In real life, a typical
problem that we would have
[53:20] might have 25 different
parties in the network.
[53:23] Might be, say, for an FX delta
30-odd different currencies that
[53:28] we've got in there.
[53:30] We pick different kinds
of hedge instruments,
[53:32] so we try and pick simple ones.
[53:34] The reason for picking things
like nondeliverable FX forwards
[53:38] is that each individual
hedge type there
[53:40] has exposure to exactly one
underlying, namely the currency.
[53:43] If I pick a dollar
euro nondeliverable,
[53:46] that's got exposure to the
dollar-euro FX rate and nothing
[53:48] but the dollar-euro FX rate
in this case, which turns out
[53:52] to be useful.
[53:54] And if you do that, you end up
with a system which is something
[53:57] like, say, 20,000 variables,
40,000 constraints.
[54:01] Something like that is the
real size of the problem.
[54:05] And really, when you're solving
convex optimization problems,
[54:10] solving convex
optimization problems
[54:12] is easy because the convex
problem looks like a bowl.
[54:14] And so they have one minimum.
[54:18] And so you can convert
the optimization problem
[54:21] into a root-finding problem,
which is find where the root
[54:25] of the derivative is--
[54:26] where the derivative
is equal to zero.
[54:29] So that's root-finding.
[54:30] People generally use
something like Newton-Raphson
[54:32] for root-finding.
[54:35] When you use
Newton-Raphson, you've
[54:37] got to compute a Hessian matrix.
[54:40] And then you need to
invert that Hessian matrix.
[54:42] That's the slow part
of the entire system
[54:44] is that you're repeatedly
inverting Hessian matrices.
[54:48] So the matrix might
be 40,000-ish.
[54:52] Matrix inversion is basically
an n cubed kind of operation.
[54:55] So you end up with this
unfeasibly large number
[54:58] of operations to solve.
[55:00] In general, most computers
will not be able to factorize
[55:04] a 40,000 matrix for a randomly
chosen 40,000 by 40,000 matrix.
[55:12] However, the problems
that we have here
[55:14] are very much not
randomly chosen matrices.
[55:18] They have an awful lot
of structure involved,
[55:20] and they're massively,
massively sparse.
[55:23] And most solvers, the reason
why they're very mature,
[55:27] is they take advantage of all
this matrix structure that's
[55:31] there.
[55:32] And so they can do
way, way, way better
[55:34] than you'd expect from this.
[55:36] So in particular, for
FX delta, the matrix
[55:40] looks a little bit
like this right.
[55:42] So you've got a bit stuff at
the top of the matrix, which
[55:45] is the thing I talked around
around the symmetry constraints
[55:48] and the flatness constraints.
[55:49] But the vast, vast
majority of the constraints
[55:52] are those ones at the bottom
of that picture, which
[55:55] are the risk
constraints specified
[55:56] by the individual parties.
[55:59] And they are guaranteed
to be block diagonal.
[56:03] Because each-- if I
have a particular hedge,
[56:06] say, the hedge AB,
that's only going
[56:09] to affect the risk between party
A and party B at worst case.
[56:13] And then the hedges
between A and C,
[56:15] they're only going to affect the
risk between parties A and C.
[56:18] So I'm definitely going to get a
block diagonal matrix down here.
[56:22] And everything else
is going to be zero.
[56:23] So the vast majority
is going to be zero.
[56:26] And if I pick these
NDF trades as well,
[56:28] and those SDF trades
only have exposure
[56:30] to one risk factor
themselves, I'm
[56:32] just going to get a straight
diagonal matrix here.
[56:34] And obviously, inverting
a straight diagonal matrix
[56:36] is trivially easy.
[56:38] So I've got a bit at
the top, which makes
[56:40] it a bit more complicated.
[56:41] But it's a little bit at
the top, plus basically
[56:44] a massive, big diagonal matrix.
[56:46] That's called a
Dantzig-Wolfe structure,
[56:48] and there are techniques
known to factorize and invert
[56:52] those kind of things.
[56:57] So then I like this slide.
[56:59] I think this is the one slide
I've used all three years.
[57:03] The problems that you
get into in real life
[57:05] are not solving the big
minimization problem.
[57:11] You just literally
write down the math
[57:13] that you want, more or less
plug that into the solver.
[57:19] But in real life,
you get situations
[57:22] where you've got
nearly parallel risks.
[57:25] You have two trades which
are nearly the same,
[57:28] but not quite exactly the
same, or can't be represented
[57:31] exactly the same on a computer.
[57:33] So this example
here, if I really
[57:36] wanted to solve this
first equation here,
[57:38] obviously everyone-- hopefully,
you can see that essentially,
[57:42] there's lots of solutions
to that right with this.
[57:46] But you can't represent a
third properly on a computer.
[57:49] So if you actually
tried to represent that
[57:52] on a computer, what
you might end up with,
[57:54] for example, instead of
putting a third, a third X1
[57:58] plus a third Y1 as
your second equation,
[58:00] you might end up with
this thing here 0.333 x1--
[58:05] sorry-- 0.3333 x1 plus 0.333 Y1.
[58:09] And that has this solution.
[58:11] 0, 1.
[58:13] But you make a tiny, tiny
change to that thing--
[58:16] so all I did was I flipped
over the solution here.
[58:21] Instead of having three 3's
at the end, having four 3's
[58:23] at the end.
[58:24] And instead of getting
a solution 0, 1,
[58:26] I've now got a solution 1, 0.
[58:28] And if I make another small
change to those things,
[58:32] it says instead of--
[58:33] I'm going to get 0.3.
[58:35] Then that has a single
solution of minus 110, 111.
[58:40] That's the solution
to that problem.
[58:43] Now, it's highly plausible
I might also say, well,
[58:45] I want all these
X's to be positive.
[58:47] That might be a thing in there.
[58:49] And so entirely due
to numerical noise,
[58:52] it will say if I want
X to be positive,
[58:53] and the only solution to this
problem is minus 110, 111,
[58:57] any system is going to go,
well, that's infeasible
[58:59] and so it will
refuse to solve it.
[59:01] And so the problems that
we get into real life
[59:05] is trying to
understand these things
[59:06] and coming up with techniques to
remove these kind of situations
[59:10] from the system,
rather than trying
[59:15] to actually solve
convex optimization
[59:18] problems in their general form.
[59:22] That's there.
[59:23] This is the same thing
as before, except now
[59:25] for the FX delta, the
full FX delta problem,
[59:29] we're up to 48 cores now.
[59:31] And you can see here,
it really was 114,000--
[59:34] it was 100,000 by 100,000 matrix
is what we ended up trying
[59:38] to solve.
[59:39] It's worth noting this presolve
thing here removed close to half
[59:44] of it.
[59:45] What presolve is,
is sometimes you
[59:47] get all these
different constraints,
[59:48] and you have them in there.
[59:49] And you end up with a constraint
that says X1 is greater than 1,
[59:52] and another one that says
X1 is greater than 2.
[59:56] So you might as well chuck
out the first constraint
[59:58] and say, well, if X1 is greater
than 1 and it's greater than 2,
[60:00] chuck out the first
one, and just keep
[60:02] the X1 is greater
than 2 constraint.
[60:04] And that happens a lot.
[60:06] And so you can massively
reduce the size.
[60:09] And so we get down
to a thing like this.
[60:12] But you can see
even this problem,
[60:14] you can solve it in 11
seconds and with very, very
[60:19] few iterations,
which is basically
[60:21] a testament to the amazing power
of Newton-Raphson quadratic
[60:26] convergence.
[60:29] So what happens when
you try and solve it?
[60:32] This is how you have
the initial risk,
[60:35] and this is with the optimized
risk on the right-hand side.
[60:37] As you might expect,
it tries to form--
[60:40] it tries to basically
get it, but I
[60:41] don't have some positive numbers
and some negative numbers.
[60:44] It tries to nestle
the risk together.
[60:45] So what you can see here.
[60:51] You try this on a
20-party system,
[60:54] again just removing
all the constraints.
[60:56] Again, it can remove
almost all the margin
[60:58] between the different systems.
[61:00] And you end up with either--
[61:01] for any given row, either
pink stuff or green stuff.
[61:05] It's either positive
or negative.
[61:06] But you don't have pink and
green stuff in the same row
[61:09] or in the same column.
[61:10] And what that says is it managed
to get rid of all the situations
[61:13] where I was up.
[61:13] I was up here and down there.
[61:15] I just want to be up or down.
[61:18] So I've netted all
the risk together.
[61:19] That's what the system was
basically trying to do.
[61:26] You try it on a real system
with all the constraints
[61:28] and stuff like that,
it's less convincing
[61:30] what it was trying to do because
the constraints hold this stuff
[61:35] in check here with their--
[61:39] Just out of interest,
this kind of diagonal
[61:42] line down the front,
that's essentially
[61:44] the margin versus itself.
[61:47] So you obviously cannot
pay margin to yourself,
[61:49] which is why you get a kind of
blank line down the diagonal.
[61:54] And the square stuff
in the middle--
[61:57] I originally thought
that was some bug.
[62:00] But what that is, is trading
between interaffiliates
[62:03] of the same entity.
[62:05] So somebody like JPMorgan
or Bank of America
[62:08] will have lots of
entities, some of which
[62:09] don't pay margin to each other.
[62:12] What I probably did here was
I ordered all the entities
[62:15] alphabetically.
[62:16] So this is probably, I'm
guessing, given I did that,
[62:20] that's probably all the
interaffiliated of JPMorgan is
[62:23] the one in the
middle since that's--
[62:25] or maybe it's Morgan Stanley.
[62:27] It'll be some company which
has got a letter roughly
[62:30] in the middle of the
alphabet with many entities
[62:33] not trading margin
versus each other.
[62:37] That's that.
[62:40] That's another example
doing interest rate stuff.
[62:44] So what we've discussed so far
is solving the optimization
[62:48] problems.
[62:49] It has to be feasible,
which means it
[62:51] satisfies all the constraints.
[62:52] And it has to be
optimal, which means
[62:54] it finds a good margin saving.
[62:58] But on top of that,
it's interesting to try
[63:01] and make them nice and
try and make them fair.
[63:05] So what a nice thing would
be is that you don't really
[63:08] want to have horrible
looking notionals.
[63:10] You don't want to
have to have a trade
[63:12] with some complicated
notional in there.
[63:15] You'd like to just trade 100
million of this or 200 million
[63:18] of that.
[63:19] The biggest amount of headache
we got into ever was trading
[63:24] with these NDF FX trades, where
we would trade it with a $1
[63:29] notional with some
200,000 million point 74,
[63:35] and then something else with the
Euros, like 0.53 in the Euros.
[63:40] And then we compute
the FX rate, which
[63:41] would be the one
divided by the other.
[63:46] And the FX rate would come out
to be a 15 decimal point number,
[63:50] and then everything
would be fine.
[63:52] And then we'd give it to the
banks, and they would complain.
[63:55] And they would say,
well, our system only
[63:57] handles six decimal places
or eight decimal places
[63:59] in the trading system.
[64:00] And when I do that, and
I put six decimal places
[64:03] in the FX rate, it
changes my euro notional.
[64:06] It gets a little bit off.
[64:07] And so we ended up having
to put notionals in that
[64:11] were round numbers of dollars.
[64:14] And that came out as an
exact round numbers of euros
[64:17] using a four decimal place
FX rate, or a six decimal
[64:20] point FX rate.
[64:22] And that turns out to be
quite tricky because you need
[64:27] to round all these numbers.
[64:29] And you can't just
take a solution
[64:31] and just round it
to the nearest ten.
[64:34] So if I have a party,
which they've got a--
[64:37] and I'm selling eight units
of something to one person,
[64:43] and I've offset
that by buying four
[64:44] units from the second person and
four units from a third person,
[64:48] everything is flat.
[64:49] But if I round everything
to the nearest 10, then
[64:52] I've rounded the 8 to 10.
[64:54] And I round both
4's down to zero.
[64:57] So now I'm no longer flat.
[64:58] So you can't do this rounding
as a post-processing step
[65:02] afterwards because it breaks the
flatness in the whole system.
[65:07] So you have to do it as
part of the optimization.
[65:10] If you do it as part
of the optimization,
[65:11] that makes it into a
mixed integer problem.
[65:13] And that makes it considerably,
considerably harder.
[65:20] People also want-- by nice, they
want a small number of trades.
[65:22] They don't want to
have to trade thousands
[65:24] and thousands of
trades in order to get
[65:26] some of this margin saving.
[65:28] They'd like to have a
small number of trades.
[65:30] We talk about it as
notional efficiency.
[65:33] And there are other
advantages of CCPs,
[65:36] I mentioned earlier, in
addition to just the netting.
[65:40] And so there's some advantage
of saying, well, I want to put--
[65:43] I'd like to put more
trades into the CCP.
[65:47] And so you might do some--
that might be a nice thing
[65:51] to have for other reasons
not directly related
[65:54] to initial margin.
[65:55] So you can add all
these niceness features
[65:57] into the system.
[65:58] The problem with adding
the nicest, things
[66:00] like round numbers,
small numbers,
[66:02] like trade counts, these
kind of things, they all
[66:04] make basically
continuous problem
[66:07] into a mixed integer problem,
which is hard to solve.
[66:15] And then fairness is--
[66:21] well, the first question
is, what does it mean?
[66:24] What does what does fairness
mean in an optimization problem?
[66:28] So you have this example.
[66:30] Hopefully, you can see this.
[66:32] This is a four-- back
to the triangle system--
[66:35] four-party system.
[66:37] It's kind of symmetric
between A and D.
[66:41] There are three possible
things you can do, all of which
[66:44] have the same
overall saving here.
[66:47] Essentially, you can ignore D,
and solve the A, B, C problem,
[66:52] in which case D gets no saving.
[66:56] You could ignore A and
get the same saving.
[67:01] Or you could kind of split
the saving between A and D.
[67:06] So they are the three
different scenarios
[67:08] that you can get right.
[67:09] So I put them down in
the table at the bottom.
[67:11] So scenario one
is the ignoring D.
[67:12] This is the saving that you get.
[67:14] A gets saving of 4.
[67:15] A, B, C, will get a saving of 4.
[67:17] D gets nothing.
[67:21] So this is-- you can
argue that's not fair
[67:27] because D gets nothing there.
[67:30] You can argue scenario 2 is not
fair because A gets nothing.
[67:34] You can argue that
of these scenarios,
[67:37] scenario 3 is the
fairest, just intuitively.
[67:43] It still might not be the
fairest because, well, why did
[67:47] A get 2 and D get 2, but B and
C got their full 4 allocation?
[67:53] So the concept of fairness
is not a well-defined one.
[67:57] One thing you can look at is--
[68:03] whoops-- have a two-step system.
[68:07] So you, first of all, figure out
what is the best possible saving
[68:11] that any one party can get.
[68:14] So the best possible saving
that all of these people can get
[68:17] is always 4.
[68:19] And so you do a whole bunch of
optimizations where you ignore
[68:23] everybody else and just
try and optimize for A.
[68:25] Then just optimize for B. Then
optimize for C. Then optimize
[68:28] for D. Now I get the
best possible thing
[68:31] that each one can be, subject
to all of the constraints
[68:34] still being there.
[68:36] When I know that, now I'm
going to say what I'm actually
[68:38] going to solve, is
how do I minimize
[68:41] the square of the difference
from my actual solution
[68:44] to those things?
[68:45] So I've got a least
squares problem
[68:47] that's in there, which
is this problem here.
[68:51] And that's the thing.
[68:52] So I'm going to do one more
optimization at the end
[68:54] when I solve that problem.
[68:56] And I'm going to say that's
the answer that I've got.
[69:00] And you can see if I
did that, in this case,
[69:02] clearly with the
squared scenario,
[69:05] 3 is going to definitely come
out as being the best solution
[69:08] because B and C will be
zero in those things.
[69:12] And then for scenario
3, I'll get 4 plus 4.
[69:18] Whereas, in scenario
1 and scenario 2,
[69:20] I will get a 16 from the square.
[69:24] So if I were to do
that on this case,
[69:28] this would be an algorithm that
would deterministically give me
[69:32] scenario 3 as the fairest.
[69:35] But there are other ways
of defining fairness.
[69:39] And I don't think it's a
well-established kind of a thing
[69:42] yet.
[69:43] I think it's the single most
interesting problem that we've
[69:46] got in the optimization space.
[69:51] And then I'll skip over.
[69:53] This is just some pictures of
what we've kind of really got
[69:55] in terms of saving.
[69:57] The more interesting
one is really
[69:59] this, which is showing the
kind of network effect.
[70:02] So you can expect,
obviously, that as I
[70:04] put more and more banks or
parties into the system,
[70:08] the savings should go up.
[70:10] That's kind of a
reasonable thing.
[70:11] But more than that, the
saving divided by the initial,
[70:16] that also goes up.
[70:17] So you get not just the
total saving in the system
[70:21] goes up, but the total--
[70:25] the efficiency increases,
the more people
[70:27] you add into the system.
[70:29] I wouldn't put too much faith
into whether it's really linear
[70:32] or whether it's a kind of
not linear thing in there.
[70:36] But there was clearly
a drift upwards
[70:39] in these things,
which basically says
[70:41] that if you want to do this, the
most effective thing you can do
[70:45] is get big networks of people.
[70:47] And big networks of people
are beneficial to everybody
[70:51] in the system.
[70:52] That's basically the story
of that picture that's there.
[70:59] I think that is the end.
[71:01] Yeah.
[71:01] So that's just a quick summary.
[71:02] We talked about value at
risk and expected shortfall.
[71:05] Talked about the centrally
cleared and bilateral.
[71:08] We talked about counterparty
risk, what variation margin is
[71:11] initial margin.
[71:12] What we're really trying to do
is optimize this initial margin.
[71:15] That basically comes down
to doing constrained convex
[71:18] optimization.
[71:19] The difficulty in
constrained optimization
[71:21] is really all the numerical
issues that you've got.
[71:25] And actually, the
interesting problems
[71:27] are not-- it's so much solving
the feasibility and optimality
[71:30] bit, but how do you add the
niceness and the fairness
[71:34] on top of that?
[71:37] Hopefully, that is the
end of your slides.
[71:41] There you go.
[71:41] Thank you very much.
[71:49] That makes sense
to anybody, or--
[71:51] [LAUGHS] anyone
have any questions?
[71:56] PROFESSOR: Go ahead.
[71:57] AUDIENCE: Yeah, I had a
question about the SIMM
[71:59] that you mentioned.
[72:00] JAMES SHEPHERD: Yeah.
[72:01] AUDIENCE: It's going to--
[72:02] like, this new thing
that's coming out and--
[72:05] JAMES SHEPHERD: Yeah.
[72:05] AUDIENCE: Is that what you said?
[72:06] JAMES SHEPHERD: Yeah.
[72:07] AUDIENCE: It's going to be
the first one where it's not
[72:09] using data from a stressful
time, like COVID, for example?
[72:15] JAMES SHEPHERD:
Yeah, yeah, yeah.
[72:17] AUDIENCE: I was wondering, what
goes into that data cut-off,
[72:21] and then what
implications do you think
[72:23] that will have for just
overall behavioral [INAUDIBLE],
[72:29] or just affecting the
economy [INAUDIBLE].
[72:32] JAMES SHEPHERD: So I don't think
it will necessarily-- well,
[72:35] the effect on the economy
is going to be-- well,
[72:37] potentially, there is going to
be a lot of margin released back
[72:39] into the system.
[72:40] So essentially, margin is money
that cannot be used for trading.
[72:44] It's essentially locked
away in segregated accounts.
[72:47] So the release of all that
margin into the system
[72:50] means there's more margin
available for trading.
[72:52] That's kind of the effect that
it would have on the system.
[72:57] In terms of the kind of
choice of parameters,
[72:59] I think effectively,
Monsieur, that really it's
[73:01] a roughly a two-year
lookback, similar to what
[73:04] I was doing in the toy
examples that I had earlier.
[73:07] So this is-- even though it's
looking at other different
[73:11] things, the stress ended roughly
'20, '21, '22-ish, something
[73:16] like that.
[73:16] So basically, it's going to be
looking at a region that's, say,
[73:20] from 2021 or 2022 beyond.
[73:23] And that's the reason that
all these big shocks that
[73:25] have happened in 2020,
they're too far in the past
[73:30] to be counted in the
correlation these days.
[73:34] Now, of course, there
might be some more.
[73:36] This exact same thing was
about to happen in 2018, 2019,
[73:40] just before that happened.
[73:41] And they would also have
been about to say, well,
[73:44] let's just smooth it all out.
[73:46] And then what did happen was
then all these shocks came in,
[73:50] and people decided that
what SIMM was doing
[73:52] was massively
underestimating the VaR.
[73:56] And the fact that they were only
recalibrating on a yearly basis
[73:59] was kind of problematic because
they had to wait a whole year,
[74:03] and in fact, a year and a
bit because of the timing
[74:05] they had in December and
the way they came out
[74:07] before they could start,
including these shocks
[74:10] that happened in 2020.
[74:14] So actually, as
a result of that,
[74:16] they moved from an annual
recalibration process
[74:18] to a semi-annual
process, so that they
[74:21] could bring the effect of
these shocks in more quickly.
[74:29] AUDIENCE: Is "they"
the regulators?
[74:30] JAMES SHEPHERD: ISDA.
[74:31] It's the International Swaps
Derivatives Association.
[74:36] So there's a panel.
[74:38] They chair it.
[74:40] It's ISDA's model.
[74:41] They're the ones who ultimately
put that thing there.
[74:43] But there's a lot of
collaboration with various banks
[74:46] and other interested parties.
[74:56] Yeah?
[74:56] AUDIENCE: I've heard recently
that there's the raising--
[75:00] like increasing
using a lever of data
[75:02] rather than just
[INAUDIBLE] the pros
[75:04] and cons of that [INAUDIBLE].
[75:06] JAMES SHEPHERD: It's
a different beta.
[75:08] AUDIENCE: OK.
[75:08] JAMES SHEPHERD: Yeah.
[75:09] So that's a beta
in terms of-- well,
[75:11] this beta here is just
a confidence interval.
[75:14] So let's just say--
[75:15] the beta is the,
I'm 99% confident
[75:18] I won't lose more than this.
[75:23] Yeah.
[75:24] AUDIENCE: Do you mind going
back to the slide where
[75:27] you talk about back testing--
[75:29] or I guess the limitations on
back testing expected shortfall.
[75:34] JAMES SHEPHERD: Yeah.
[75:36] Hang on.
[75:38] That one.
[75:39] AUDIENCE: Yeah, I guess it was--
[75:45] I guess in my--
[75:48] what are some ways that
you can almost cut corners,
[75:51] like make some assumptions
that allow you to calculate
[75:56] expected shortfall.
[75:58] What do you have to assume
for it to be possible to do?
[76:01] JAMES SHEPHERD: To be
possible to back test?
[76:04] AUDIENCE: [INAUDIBLE], yeah.
[76:06] JAMES SHEPHERD: Well, you
have to make some assumptions
[76:10] around the form of the tail.
[76:12] So if you were to say, well,
the tail is kind of flat,
[76:15] or you have some
structure in that thing,
[76:17] you could start to say,
does it fit in there?
[76:20] What normally
happens in real life
[76:23] is that regulators have
moved from VaR from saying,
[76:27] well, your actual initial margin
and capital should be based--
[76:31] that used to be VaR.
[76:32] Then it was stress-VaR,
and now it's
[76:34] moved to expected shortfall.
[76:36] But they still require
you to back test VaR
[76:39] So what you generally
do is you build
[76:40] a model, which
contains-- which will
[76:43] predict both VaR and
expected shortfall.
[76:45] You compute the number using
the expected shortfall number.
[76:48] And then you back test the VaR
because that's a little easier.
[76:51] And then you say, well I've
built the model consistently.
[76:53] And all I did was apply
a different multiplier
[76:55] for the expected
shortfall versus the VaR.
[76:57] So if the VaR back
tests properly,
[76:59] then I'm prepared to accept
the expected shortfall.
[77:05] AUDIENCE: Right.
[77:07] If you assume a different
shape in the tails,
[77:10] then theoretically
that's not necessarily
[77:13] a valid statistical test.
[77:17] Is that [INAUDIBLE]?
[77:17] JAMES SHEPHERD: Well, it is.
[77:19] But when you're back testing--
[77:20] you're back testing,
and you say, well,
[77:22] what happened on the
23rd of December 2015?
[77:26] Well, there was no distribution.
[77:27] That's just whatever
happened on that date.
[77:29] So there's no
distribution there.
[77:31] So you can't say--
[77:32] it's difficult to make an
assumption about whether or not
[77:36] that was kind of predicted
or not predicted.
[77:40] Because it just--
it's a single draw
[77:44] from the distribution
as opposed to the shape
[77:47] of the distribution.
[77:47] It doesn't tell you anything.
[77:49] You can make any assumption
you want about the tail.
[77:51] But because I've
taken one number,
[77:53] it doesn't really
show me anything.
[77:55] Does that make sense?
[77:56] AUDIENCE: Yeah.
[77:57] JAMES SHEPHERD: Yeah?
[77:59] AUDIENCE: I guess
building on from that,
[78:01] so you mentioned that you can
back past on both the shortfall
[78:05] and bar on bar instead
of a shortfall?
[78:07] And that's kind of like
this-- and then helps you
[78:11] like predict more accurately.
[78:13] Are these models accurate
enough to account
[78:16] for the difference
[INAUDIBLE] of somewhere
[78:19] between bar and shortfall?
[78:21] Are they precise enough to you?
[78:23] JAMES SHEPHERD:
Are they-- well, it
[78:25] depends how you
build up the model.
[78:26] So essentially, my model here--
[78:28] the model wasn't really a VaR
model or an expected shortfall
[78:31] model.
[78:32] The model that I proposed
here was that everything--
[78:36] that the daily changes
are normally distributed.
[78:39] And in this case, that
they're independent--
[78:42] all the daily changes
are independent.
[78:44] That was essentially my model.
[78:47] Having made that assumption, I
get a VaR number and an expected
[78:50] shortfall number, and I
can back test the VaR.
[78:53] In real life, people make
more sophisticated choices.
[78:56] They don't assume that
it's normally distributed.
[78:58] You can have other
distributions.
[79:00] You don't assume that
all the changes are
[79:03] independent of each
other, but the model
[79:06] is not really a VaR model
necessarily, or an expected
[79:08] shortfall model.
[79:09] The model is, what did I
assume about the distribution?
[79:13] Having made those assumptions,
I get a VAR number
[79:16] and I get an expected
shortfall number.
[79:18] Does that make sense?
[79:21] AUDIENCE: On this example,
when you were explaining it,
[79:24] you said that--
[79:27] let's see.
[79:27] I guess the actual shortfall was
5.2%, was it, through the mod--
[79:34] or through the
historical simulation.
[79:37] JAMES SHEPHERD: Yeah.
[79:38] So what it said was that this
came up-- so the VaR came up
[79:43] as 2.25, based on the model.
[79:45] If I go back to this table--
[79:47] so this is the
leftmost column here.
[79:50] In reality, we can see that
there were 12 actual days when
[79:57] I exceeded that number.
[79:59] There should have been five.
[80:00] That was the intention.
[80:01] So you say, but if I
was trying to produce
[80:04] something that had a 1%--
[80:07] I'm supposed to exceed
VaR 1% of the time.
[80:10] That's the definition of VaR.
[80:13] So if I'm trying to come up with
a model where I expect something
[80:17] to happen 1% of the time, or I
expect the VaR to be exceeded
[80:21] 1% of the time, then I do 500
draws of that thing, and I say,
[80:28] well, how many times was
it actually exceeded?
[80:31] And then the probability
of that being 12 is 5%.
[80:34] AUDIENCE: So you are
being conservative.
[80:36] Like this--
[80:37] JAMES SHEPHERD: Yes.
[80:37] AUDIENCE: This VaR
is conservative.
[80:39] Therefore, it's OK.
[80:40] Even though it's wrong
in a sense, or at least
[80:43] it's not calibrated.
[80:43] But it's conservative.
[80:46] JAMES SHEPHERD: It's
not that conservative.
[80:48] A conservative VaR would be
bigger than the historical VaR.
[80:52] So the actual thing
is the historical VaR
[80:54] was 300 or something.
[80:56] Conservative would
be a bigger number.
[80:59] But it's not overly
aggressive, let's say.
[81:03] I think that's probably
the way to put it.
[81:07] PROFESSOR: Any other questions?
[81:10] Anyway, thanks very much, again.
[81:11] JAMES SHEPHERD: OK.
[81:11] Thank you.
