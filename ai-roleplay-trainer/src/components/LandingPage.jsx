import React, { useState, useEffect } from 'react';
import emailjs from 'emailjs-com';
import { ChevronRight, Users, Target, TrendingUp, MessageCircle, Award, CheckCircle, ArrowRight, Zap, Brain, Shield, UserX, BookOpen, Video } from 'lucide-react';

const LandingPage = () => {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    emailjs.send(
      'service_el8ixrs',      // Replace with your EmailJS service ID
      'template_t7wts2m',     // Replace with your EmailJS template ID
      {
        user_email: email,
        message: `New beta signup from ${email}`,
        to_name: 'AI Roleplay Trainer Team'
      },
      'nmG_8kMJ6PofAHE3-'       // Replace with your EmailJS public key
    )
    .then(() => {
      setIsSubmitted(true);
      setEmail('');
      console.log('Email sent successfully!');
    })
    .catch((error) => {
      console.error('Email failed to send:', error);
      // Handle error (maybe show error message to user)
    });
  };

  const scrollToCta = () => {
    const ctaSection = document.getElementById('cta');
    if (ctaSection) {
      ctaSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white overflow-x-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0">
        <div 
          className="absolute inset-0 opacity-20"
          style={{
            background: `radial-gradient(circle at ${50 + scrollY * 0.02}% ${50 + scrollY * 0.01}%, rgba(102, 126, 234, 0.3) 0%, transparent 50%)`,
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-blue-900/20" />
      </div>

      {/* Hero Section */}
      <section className="relative z-10 min-h-screen flex items-center justify-center px-6">
        <div className="max-w-6xl mx-auto text-center">
          <div 
            className="transform transition-all duration-1000 ease-out"
            style={{ 
              transform: `translateY(${-scrollY * 0.3}px)`,
              opacity: Math.max(0, 1 - scrollY * 0.002)
            }}
          >
            <div className="inline-block mb-6 px-4 py-2 bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-full border border-purple-500/30 backdrop-blur-sm">
              <span className="text-sm font-medium text-purple-300">🚀 Vision Stage: Seeking Early Adopters</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent leading-tight">
              Master High-Stakes Conversations with an{' '}
              <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                AI Conversation Coach
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-300 mb-12 max-w-4xl mx-auto leading-relaxed">
              Practice job interviews, difficult conversations, and leadership scenarios with an AI that gives you instant, private feedback. Build the confidence to handle any situation.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <button onClick={scrollToCta} className="group px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/25">
                Request Early Access
                <ArrowRight className="inline-block ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </div>
            
            <div className="mt-16 flex items-center justify-center gap-8 text-sm text-slate-400">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                No credit card required
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                Influence the product roadmap
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                Get free access at launch
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-12">
            Do High-Stakes Conversations <span className="text-red-400">Hold You Back</span>?
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            {[
              { icon: "😰", title: "Interview Anxiety", desc: "Struggling to articulate your value under pressure and land your dream job." },
              { icon: "😬", title: "Leadership Challenges", desc: "Finding it tough to give difficult feedback or motivate your team effectively." },
              { icon: "😤", title: "Difficult Customers", desc: "Losing your cool when dealing with frustrated clients, impacting satisfaction." },
              { icon: "😔", title: "Missed Opportunities", desc: "Lacking the confidence to speak up, negotiate, or build key relationships." }
            ].map((item, index) => (
              <div key={index} className="p-6 bg-white/5 backdrop-blur-sm border border-red-500/20 rounded-2xl transform hover:scale-105 transition-all duration-300">
                <div className="text-4xl mb-4">{item.icon}</div>
                <h3 className="text-xl font-semibold mb-3 text-red-300">{item.title}</h3>
                <p className="text-slate-300">{item.desc}</p>
              </div>
            ))}
          </div>
          
          <p className="text-xl text-slate-300">
            <strong className="text-purple-300">You're not alone.</strong> Key conversations can be daunting, but they are skills you can learn and master.
          </p>
        </div>
      </section>

      {/* Solution Section */}
      <section className="relative z-10 py-24 px-6 bg-gradient-to-r from-purple-900/20 to-blue-900/20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Practice in a <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">Safe Space</span>, 
              Succeed in the <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Real World</span>
            </h2>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              Our AI Roleplay Trainer provides a private, judgment-free zone to practice, make mistakes, and get actionable feedback to build real-world confidence.
            </p>
          </div>

          {/* Interactive Demo Mockup */}
          <div className="max-w-4xl mx-auto mb-16">
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-600 rounded-2xl p-6 shadow-2xl">
              <div className="flex items-center gap-3 mb-6 border-b border-slate-600 pb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                  <Users className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold">Alex - Underperforming Team Member</h3>
                  <p className="text-sm text-slate-400">Manager Feedback Scenario</p>
                </div>
                <div className="ml-auto px-3 py-1 bg-green-500/20 text-green-300 text-sm rounded-full border border-green-500/30">
                  Live Session
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex-shrink-0"></div>
                  <div className="bg-slate-700 rounded-lg p-3 max-w-xs">
                    <p className="text-sm">"Alex, I wanted to chat about your recent performance on the project. I've noticed a few deadlines have slipped."</p>
                  </div>
                </div>
                
                <div className="flex gap-3 justify-end">
                  <div className="bg-blue-600 rounded-lg p-3 max-w-xs">
                    <p className="text-sm">"I know, I've been feeling a bit overwhelmed with the workload recently."</p>
                  </div>
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex-shrink-0"></div>
                </div>
                
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex-shrink-0"></div>
                  <div className="bg-slate-700 rounded-lg p-3 max-w-xs">
                    <p className="text-sm">"I understand. Let's talk about how we can better support you. What's been the biggest challenge?"</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-green-900/30 to-blue-900/30 rounded-xl p-4 border border-green-500/20">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-green-300">Performance Analysis</h4>
                  <div className="text-2xl font-bold text-green-400">8.2/10</div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-green-300 font-medium">Strengths:</p>
                    <p className="text-slate-300">Empathetic tone, open-ended questions</p>
                  </div>
                  <div>
                    <p className="text-yellow-300 font-medium">Improve:</p>
                    <p className="text-slate-300">Define clearer next steps</p>
                  </div>
                  <div>
                    <p className="text-blue-300 font-medium">Next Focus:</p>
                    <p className="text-slate-300">Active listening skills</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            How It <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Works</span>
          </h2>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { icon: Target, title: "1. Choose Your Scenario", desc: "Select from a library of common challenges for managers, professionals, and individuals." },
              { icon: MessageCircle, title: "2. Talk with the AI", desc: "Engage in realistic, text-based conversations with an adaptive AI persona." },
              { icon: Brain, title: "3. Get Instant Feedback", desc: "Receive a detailed analysis of your performance with actionable, private insights." },
              { icon: TrendingUp, title: "4. Track Your Growth", desc: "Watch your skills and confidence improve over time with every session." }
            ].map((step, index) => (
              <div key={index} className="text-center group">
                <div className="relative mb-6">
                  <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                    <step.icon className="w-8 h-8" />
                  </div>
                  {index < 3 && (
                    <div className="hidden md:block absolute top-8 left-full w-full">
                      <ArrowRight className="w-6 h-6 text-slate-500 mx-auto" />
                    </div>
                  )}
                </div>
                <h3 className="text-xl font-semibold mb-3">{step.title}</h3>
                <p className="text-slate-300">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative z-10 py-24 px-6 bg-gradient-to-r from-slate-900 to-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              A Personal Coach for <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Every Conversation</span>
            </h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Zap, title: "Realistic AI Personas", desc: "Practice with AI that adapts to your tone and provides challenging, true-to-life conversation.", color: "from-yellow-400 to-orange-400" },
              { icon: Award, title: "Behavioral Analysis", desc: "Get feedback based on proven behavioral science to drive real improvement.", color: "from-green-400 to-emerald-400" },
              { icon: Shield, title: "Completely Private", desc: "Practice sensitive conversations with the confidence that your data is secure and never shared.", color: "from-blue-400 to-cyan-400" }
            ].map((feature, index) => (
              <div key={index} className="group p-8 bg-white/5 backdrop-blur-sm border border-slate-600 rounded-2xl hover:bg-white/10 transition-all duration-300 transform hover:scale-105">
                <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-4">{feature.title}</h3>
                <p className="text-slate-300">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Traditional Practice Falls Short */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Why Traditional Practice <span className="text-red-400">Falls Short</span>
            </h2>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              Traditional methods often lack the realism, privacy, and objective feedback needed for true growth. We bridge that gap.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { icon: UserX, title: "Mirror Practice", desc: "No real interaction or feedback. You're talking to yourself, not a dynamic partner." },
              { icon: Users, title: "Friends & Colleagues", desc: "Feedback can be biased, uncomfortable, or lack expert insight. Limited availability." },
              { icon: BookOpen, title: "Reading & Courses", desc: "Passive learning. Knowledge without practice doesn't translate to real-world skill." },
              { icon: Video, title: "Watching Videos", desc: "Observational learning is helpful, but it's not a substitute for active, hands-on practice." }
            ].map((item, index) => (
              <div key={index} className="group p-6 bg-white/5 backdrop-blur-sm border border-slate-600 rounded-2xl hover:bg-white/10 transition-all duration-300 transform hover:scale-105">
                <div className="w-12 h-12 bg-gradient-to-r from-red-600 to-orange-600 rounded-xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                  <item.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-4">{item.title}</h3>
                <p className="text-slate-300">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* The Science Behind Your Success */}
      <section className="relative z-10 py-24 px-6 bg-gradient-to-r from-purple-900/20 to-blue-900/20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              The Science Behind Your <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">Success</span>
            </h2>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              Our platform is built on proven psychological principles to ensure effective and lasting communication skill development.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { icon: Brain, title: "Active Recall", desc: "Engage in active conversation, not passive consumption, for stronger memory and skill retention." },
              { icon: MessageCircle, title: "Immediate Feedback", desc: "Receive instant, actionable insights to quickly correct mistakes and reinforce effective strategies." },
              { icon: TrendingUp, title: "Spaced Repetition", desc: "Revisit scenarios over time to embed new communication habits into your long-term memory." },
              { icon: Shield, title: "Psychological Safety", desc: "Practice in a private, judgment-free space, allowing you to experiment and grow without fear." }
            ].map((item, index) => (
              <div key={index} className="group p-6 bg-white/5 backdrop-blur-sm border border-slate-600 rounded-2xl hover:bg-white/10 transition-all duration-300 transform hover:scale-105">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl flex items-center justify-center mb-6 group-hover:rotate-6 transition-transform">
                  <item.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold mb-4">{item.title}</h3>
                <p className="text-slate-300">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="cta" className="relative z-10 py-24 px-6 bg-gradient-to-r from-purple-900/30 to-blue-900/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Become a <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Founding User</span>
          </h2>
          
          <p className="text-xl text-slate-300 mb-12">
            We're looking for ambitious professionals and managers to help shape the future of conversation coaching. Join our beta to get early access and help us build the best tool for you.
          </p>
          
          {!isSubmitted ? (
            <form onSubmit={handleSubmit} className="max-w-md mx-auto">
              <div className="flex gap-4 mb-6">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email address"
                  className="flex-1 px-6 py-4 bg-white/10 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 backdrop-blur-sm"
                  required
                />
                <button
                  type="submit"
                  className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 whitespace-nowrap"
                >
                  Request Access
                </button>
              </div>
              
              <p className="text-sm text-slate-400">
                Free beta access • No credit card required
              </p>
            </form>
          ) : (
            <div className="max-w-md mx-auto p-6 bg-green-900/20 border border-green-500/30 rounded-2xl backdrop-blur-sm">
              <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-green-300 mb-2">You're on the list!</h3>
              <p className="text-slate-300">Thank you for your interest. We'll be in touch soon with an invitation to join the beta.</p>
            </div>
          )}
        </div>
      </section>

      {/* FAQ Section */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            Frequently Asked <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Questions</span>
          </h2>
          
          <div className="space-y-6">
            {[
              {
                q: "What is AI Roleplay Trainer?",
                a: "It's a web application that lets you practice important conversations with an AI partner. It's designed to help you build confidence and communication skills for professional and personal situations in a private, judgment-free environment."
              },
              {
                q: "How does the AI work?",
                a: "Our AI is trained on vast datasets of conversations to provide realistic, adaptive responses. It analyzes your word choice, tone (inferred from text), and strategy to give you targeted feedback on how to improve."
              },
              {
                q: "Who is this for?",
                a: "It's for anyone who wants to improve their communication skills. This includes ambitious professionals preparing for interviews, managers learning to lead difficult conversations, and individuals looking to boost their social confidence."
              },
              {
                q: "Is my practice data private?",
                a: "Yes. Your privacy is our top priority. All conversations are encrypted and stored securely. We will never share your practice sessions. You will have full control over your data."
              },
              {
                q: "How can I get involved?",
                a: "We are currently in our vision stage and looking for founding users to help us test and refine the product. You can sign up for early access using the form above. We'd love to hear your feedback."
              }
            ].map((faq, index) => (
              <div key={index} className="bg-white/5 backdrop-blur-sm border border-slate-600 rounded-2xl p-6 hover:bg-white/10 transition-colors">
                <h3 className="text-lg font-semibold mb-3 text-purple-300">{faq.q}</h3>
                <p className="text-slate-300 leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 py-16 px-6 border-t border-slate-800">
        <div className="max-w-6xl mx-auto">
          <div className="text-center">
            <p className="text-slate-400">
              © 2025 AI Roleplay Trainer. All rights reserved. 
            </p>
          </div>
        </div>
      </footer>

      {/* Floating CTA */}
      <div className="fixed bottom-6 right-6 z-50">
        <button onClick={scrollToCta} className="group px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-full font-semibold shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 transform hover:scale-105">
          <span className="mr-2">🚀</span>
          Request Access
          <ChevronRight className="inline-block ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

export default LandingPage;