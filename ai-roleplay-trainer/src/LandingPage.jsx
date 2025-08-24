import React, { useState, useEffect } from 'react';
import { ChevronRight, Play, Users, Target, TrendingUp, Star, MessageCircle, Award, CheckCircle, ArrowRight, Zap, Brain, Shield } from 'lucide-react';

const LandingPage = () => {
  const [email, setEmail] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [scrollY, setScrollY] = useState(0);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  const testimonials = [
    {
      name: "Sarah M.",
      role: "Marketing Manager",
      content: "Landed my dream job after practicing with AI personas. The interview feedback was incredibly detailed and helped me identify exactly what I needed to improve.",
      rating: 5
    },
    {
      name: "David L.",
      role: "Sales Representative",
      content: "My customer satisfaction scores improved by 40% after using the difficult customer scenarios. The AI personas felt so realistic!",
      rating: 5
    },
    {
      name: "Emma R.",
      role: "Recent Graduate",
      content: "Finally feel confident networking. The AI helped me practice small talk and conversation starters without any judgment.",
      rating: 5
    }
  ];

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Auto-rotate testimonials
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(timer);
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
              <span className="text-sm font-medium text-purple-300">🚀 Now in Beta Testing</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent leading-tight">
              Master Any Conversation with{' '}
              <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                AI-Powered Training
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-slate-300 mb-12 max-w-4xl mx-auto leading-relaxed">
              Practice job interviews, difficult customer interactions, and social situations with personalized AI personas. 
              Get instant feedback and build unshakeable confidence.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <button className="group px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-xl font-semibold text-lg transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/25">
                Start Training for Free
                <ArrowRight className="inline-block ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              
              <button className="group flex items-center px-6 py-4 border border-slate-600 hover:border-slate-400 rounded-xl font-medium transition-all duration-300 hover:bg-white/5">
                <Play className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
                Watch Demo
              </button>
            </div>
            
            <div className="mt-16 flex items-center justify-center gap-8 text-sm text-slate-400">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                No credit card required
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                5-minute setup
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                Instant feedback
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-12">
            Struggling with <span className="text-red-400">High-Stakes Conversations</span>?
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8 mb-16">
            {[
              { icon: "😰", title: "Interview Anxiety", desc: "Sweaty palms and racing thoughts before important job interviews" },
              { icon: "😬", title: "Awkward Networking", desc: "Uncomfortable silence and struggling to make meaningful connections" },
              { icon: "😤", title: "Difficult Customers", desc: "Losing composure when dealing with frustrated or angry clients" },
              { icon: "😔", title: "Missed Opportunities", desc: "Watching promotions and relationships slip away due to poor communication" }
            ].map((item, index) => (
              <div key={index} className="p-6 bg-white/5 backdrop-blur-sm border border-red-500/20 rounded-2xl transform hover:scale-105 transition-all duration-300">
                <div className="text-4xl mb-4">{item.icon}</div>
                <h3 className="text-xl font-semibold mb-3 text-red-300">{item.title}</h3>
                <p className="text-slate-300">{item.desc}</p>
              </div>
            ))}
          </div>
          
          <p className="text-xl text-slate-300">
            <strong className="text-purple-300">You're not alone.</strong> 75% of people experience communication anxiety that holds them back from reaching their full potential.
          </p>
        </div>
      </section>

      {/* Solution Section */}
      <section className="relative z-10 py-24 px-6 bg-gradient-to-r from-purple-900/20 to-blue-900/20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Train Like a <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Pro</span>, 
              Perform Like a <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">Champion</span>
            </h2>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">
              Practice in a safe environment with AI personas that adapt to your style. Get detailed feedback and track your progress.
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
                  <h3 className="font-semibold">Sarah - HR Manager</h3>
                  <p className="text-sm text-slate-400">Job Interview Scenario</p>
                </div>
                <div className="ml-auto px-3 py-1 bg-green-500/20 text-green-300 text-sm rounded-full border border-green-500/30">
                  Live Session
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex-shrink-0"></div>
                  <div className="bg-slate-700 rounded-lg p-3 max-w-xs">
                    <p className="text-sm">Tell me about a time you handled a challenging project.</p>
                  </div>
                </div>
                
                <div className="flex gap-3 justify-end">
                  <div className="bg-blue-600 rounded-lg p-3 max-w-xs">
                    <p className="text-sm">I led a team of 5 developers to deliver a complex web application under a tight deadline...</p>
                  </div>
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex-shrink-0"></div>
                </div>
                
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex-shrink-0"></div>
                  <div className="bg-slate-700 rounded-lg p-3 max-w-xs">
                    <p className="text-sm">That sounds impressive! What was the biggest challenge you faced?</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-gradient-to-r from-green-900/30 to-blue-900/30 rounded-xl p-4 border border-green-500/20">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-green-300">Performance Analysis</h4>
                  <div className="text-2xl font-bold text-green-400">8.7/10</div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-green-300 font-medium">Strengths:</p>
                    <p className="text-slate-300">Clear structure, specific examples</p>
                  </div>
                  <div>
                    <p className="text-yellow-300 font-medium">Improve:</p>
                    <p className="text-slate-300">Add more emotional context</p>
                  </div>
                  <div>
                    <p className="text-blue-300 font-medium">Next Focus:</p>
                    <p className="text-slate-300">Body language awareness</p>
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
              { icon: Target, title: "Choose Scenario", desc: "Pick from job interviews, customer service, networking, or social situations" },
              { icon: MessageCircle, title: "Chat with AI", desc: "Engage with realistic AI personas that adapt to your communication style" },
              { icon: Brain, title: "Get Feedback", desc: "Receive detailed analysis of your performance with actionable insights" },
              { icon: TrendingUp, title: "Track Progress", desc: "Monitor your improvement over time and master new scenarios" }
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
              Powerful Features for <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Real Results</span>
            </h2>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Zap, title: "AI-Powered Personas", desc: "Realistic conversation partners with distinct personalities and adaptive responses", color: "from-yellow-400 to-orange-400" },
              { icon: Award, title: "Detailed Analytics", desc: "Performance scoring, conversation analysis, and personalized improvement recommendations", color: "from-green-400 to-emerald-400" },
              { icon: Shield, title: "Safe Practice Space", desc: "No judgment, unlimited retries, and complete privacy for confident learning", color: "from-blue-400 to-cyan-400" }
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

      {/* Testimonials */}
      <section className="relative z-10 py-24 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">
            What Our <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Users Say</span>
          </h2>
          
          <div className="relative">
            <div className="bg-white/5 backdrop-blur-sm border border-slate-600 rounded-2xl p-8 text-center">
              <div className="flex justify-center mb-4">
                {[...Array(testimonials[currentTestimonial].rating)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                ))}
              </div>
              
              <blockquote className="text-xl text-slate-200 mb-6 leading-relaxed">
                "{testimonials[currentTestimonial].content}"
              </blockquote>
              
              <div className="font-semibold text-purple-300">
                {testimonials[currentTestimonial].name}
              </div>
              <div className="text-slate-400">
                {testimonials[currentTestimonial].role}
              </div>
            </div>
            
            <div className="flex justify-center mt-6 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  className={`w-3 h-3 rounded-full transition-colors ${
                    index === currentTestimonial ? 'bg-purple-500' : 'bg-slate-600'
                  }`}
                  onClick={() => setCurrentTestimonial(index)}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-24 px-6 bg-gradient-to-r from-purple-900/30 to-blue-900/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">Communication Skills</span>?
          </h2>
          
          <p className="text-xl text-slate-300 mb-12">
            Join thousands of professionals who've already improved their confidence and career prospects.
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
                  Get Started
                </button>
              </div>
              
              <p className="text-sm text-slate-400">
                Free beta access • No credit card required • Cancel anytime
              </p>
            </form>
          ) : (
            <div className="max-w-md mx-auto p-6 bg-green-900/20 border border-green-500/30 rounded-2xl backdrop-blur-sm">
              <CheckCircle className="w-12 h-12 text-green-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-green-300 mb-2">Thank You!</h3>
              <p className="text-slate-300">We'll notify you when beta access is available. Check your email for your free communication guide!</p>
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
                q: "How realistic are the AI personas?",
                a: "Our AI personas are trained on thousands of real conversations and adapt to your communication style. They provide realistic responses that mirror actual human interactions in various professional and social contexts."
              },
              {
                q: "What scenarios can I practice?",
                a: "Choose from job interviews, salary negotiations, customer service interactions, networking events, first dates, difficult conversations, and more. We're constantly adding new scenarios based on user feedback."
              },
              {
                q: "How does the feedback system work?",
                a: "Our AI analyzes your conversation in real-time, evaluating factors like clarity, confidence, empathy, and effectiveness. You receive detailed insights on strengths, areas for improvement, and specific actionable recommendations."
              },
              {
                q: "Is my practice data private and secure?",
                a: "Absolutely. All your conversations and personal data are encrypted and stored securely. We never share your practice sessions with anyone, and you can delete your data at any time."
              },
              {
                q: "Can I track my progress over time?",
                a: "Yes! Your performance dashboard shows improvement trends, skill development, and achievement milestones. You can review past sessions and see how your communication skills evolve."
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
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-4">
              AI Roleplay Trainer
            </h3>
            <p className="text-slate-400 max-w-md mx-auto">
              Master conversations, build confidence, and unlock your potential with AI-powered communication training.
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <h4 className="font-semibold mb-4 text-slate-300">Product</h4>
              <ul className="space-y-2 text-slate-400">
                <li><button type="button" className="hover:text-white transition-colors">Features</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Scenarios</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Pricing</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Beta Access</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4 text-slate-300">Resources</h4>
              <ul className="space-y-2 text-slate-400">
                <li><button type="button" className="hover:text-white transition-colors">Blog</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Help Center</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Community</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Success Stories</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4 text-slate-300">Company</h4>
              <ul className="space-y-2 text-slate-400">
                <li><button type="button" className="hover:text-white transition-colors">About</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Careers</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Contact</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Partners</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4 text-slate-300">Legal</h4>
              <ul className="space-y-2 text-slate-400">
                <li><button type="button" className="hover:text-white transition-colors">Privacy Policy</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Terms of Service</button></li>
                <li><button type="button" className="hover:text-white transition-colors">Security</button></li>
                <li><button type="button" className="hover:text-white transition-colors">GDPR</button></li>
              </ul>
            </div>
          </div>
          
          <div className="text-center pt-8 border-t border-slate-800">
            <p className="text-slate-400">
              © 2025 AI Roleplay Trainer. All rights reserved. 
              <span className="ml-4 text-slate-500">
                Built with ❤️ for better communication
              </span>
            </p>
          </div>
        </div>
      </footer>

      {/* Floating CTA */}
      <div className="fixed bottom-6 right-6 z-50">
        <button className="group px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 rounded-full font-semibold shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 transform hover:scale-105">
          <span className="mr-2">🚀</span>
          Start Training
          <ChevronRight className="inline-block ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </button>
      </div>
    </div>
  );
};

export default LandingPage;