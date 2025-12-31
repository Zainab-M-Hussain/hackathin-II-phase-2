"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { motion } from "framer-motion";
import DarkModeToggle from "@/app/components/DarkModeToggle";
import MenuIcon from "@/app/components/icons/MenuIcon";
import CloseIcon from "@/app/components/icons/CloseIcon";
import FloatingChatWidget from "@/app/components/FloatingChatWidget";

export default function HomePage() {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLoginClick = () => {
    router.push("/login");
  };

  const handleSignupClick = () => {
    router.push("/signup");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-900/20 to-black text-white">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1/3 bg-gradient-to-b from-indigo-500/10 to-transparent"></div>
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-72 h-72 bg-gray-500/5 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-20 px-6 py-6">
        <div className="container mx-auto flex justify-between items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="text-2xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent"
          >
            FlowTask
          </motion.div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-6">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push("/chat")}
              className="px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 transition-all duration-300 font-medium shadow-lg hover:shadow-indigo-500/25"
            >
              Flow Assistant
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push("/dashboard")}
              className="text-gray-300 hover:text-white transition-colors font-medium"
            >
              Dashboard
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLoginClick}
              className="px-4 py-2 rounded-lg bg-gray-800/50 hover:bg-indigo-600/20 border border-gray-700 hover:border-indigo-500/50 transition-all duration-300 font-medium"
            >
              Login
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSignupClick}
              className="px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 transition-all duration-300 font-medium shadow-lg hover:shadow-indigo-500/25"
            >
              Sign Up
            </motion.button>
            <DarkModeToggle />
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="z-50 text-white"
            >
              {isMenuOpen ? <CloseIcon /> : <MenuIcon />}
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          className="md:hidden absolute top-0 left-0 w-full h-screen bg-gray-900/90 backdrop-blur-lg z-40 flex flex-col items-center justify-center gap-8"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              router.push("/chat");
              setIsMenuOpen(false);
            }}
            className="text-2xl px-6 py-3 rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 transition-all duration-300 font-medium shadow-lg hover:shadow-indigo-500/25"
          >
            Flow Assistant
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              router.push("/dashboard");
              setIsMenuOpen(false);
            }}
            className="text-2xl text-gray-300 hover:text-white transition-colors font-medium"
          >
            Dashboard
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              handleLoginClick();
              setIsMenuOpen(false);
            }}
            className="text-2xl px-6 py-3 rounded-lg bg-gray-800/50 hover:bg-indigo-600/20 border border-gray-700 hover:border-indigo-500/50 transition-all duration-300 font-medium"
          >
            Login
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              handleSignupClick();
              setIsMenuOpen(false);
            }}
            className="text-2xl px-6 py-3 rounded-lg bg-gradient-to-r from-indigo-600 to-indigo-700 hover:from-indigo-500 hover:to-indigo-600 transition-all duration-300 font-medium shadow-lg hover:shadow-indigo-500/25"
          >
            Sign Up
          </motion.button>
          <div className="mt-4">
            <DarkModeToggle />
          </div>
        </motion.div>
      )}

      {/* Hero Section */}
      <main className="relative z-10 px-6 py-12">
        <div className="container mx-auto max-w-7xl">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="text-center lg:text-left"
            >
              <motion.div
                className="inline-block mb-6"
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.6, type: "spring", stiffness: 100 }}
              >
                <span className="px-4 py-2 rounded-full bg-indigo-500/20 text-indigo-300 text-sm font-medium border border-indigo-500/30 backdrop-blur-sm">
                  Productivity Reimagined
                </span>
              </motion.div>

              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
                <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400 bg-clip-text text-transparent">
                  Transform Your
                </span>
                <br />
                <span className="text-white">Workflow Today</span>
              </h1>

              <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto lg:mx-0">
                The all-in-one platform that helps teams organize, prioritize, and execute tasks with unprecedented efficiency.
              </p>

              <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSignupClick}
                  className="btn btn-primary px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300"
                >
                  Get Started
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => router.push("/chat")}
                  className="btn btn-outline px-8 py-4 rounded-xl text-lg font-medium transition-all duration-300"
                >
                  Try Flow Assistant
                </motion.button>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="relative"
            >
              <div className="relative rounded-3xl overflow-hidden border border-gray-700/50 bg-gradient-to-br from-gray-800/30 to-gray-900/50 p-8 backdrop-blur-sm">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5"></div>
                <div className="relative z-10">
                  <div className="flex justify-between items-center mb-6">
                    <div className="text-lg font-bold text-indigo-400">Dashboard Overview</div>
                    <div className="flex space-x-2">
                      <div className="w-3 h-3 rounded-full bg-red-500"></div>
                      <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                      <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="p-4 bg-gray-800/50 rounded-xl border border-gray-700/30">
                      <div className="flex justify-between items-center">
                        <div className="font-medium">Project Alpha</div>
                        <div className="text-sm text-gray-400">85% Complete</div>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                        <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                      </div>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-xl border border-gray-700/30">
                      <div className="flex justify-between items-center">
                        <div className="font-medium">Marketing Campaign</div>
                        <div className="text-sm text-gray-400">60% Complete</div>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                        <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full" style={{ width: '60%' }}></div>
                      </div>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-xl border border-gray-700/30">
                      <div className="flex justify-between items-center">
                        <div className="font-medium">Product Launch</div>
                        <div className="text-sm text-gray-400">30% Complete</div>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
                        <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full" style={{ width: '30%' }}></div>
                      </div>
                    </div>
                  </div>

                  <div className="mt-8 pt-6 border-t border-gray-700/50">
                    <div className="flex items-center justify-between">
                      <div className="text-gray-400">Tasks Completed</div>
                      <div className="text-2xl font-bold text-white">24/30</div>
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                      <div className="text-gray-400">Upcoming Deadlines</div>
                      <div className="text-xl font-bold text-white">5</div>
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </main>

      {/* Stats Section */}
      <section className="relative z-10 py-16">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-6xl mx-auto">
            {[
              { value: "95%", label: "Task Completion" },
              { value: "40%", label: "Time Saved" },
              { value: "10k+", label: "Active Users" },
              { value: "24/7", label: "Support" }
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 * index, duration: 0.5 }}
                className="text-center"
              >
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent mb-2">
                  {stat.value}
                </div>
                <div className="text-gray-400 text-sm md:text-base">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="relative z-10 py-20">
        <div className="container mx-auto px-6">
          <motion.div
            className="text-center mb-16 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Everything You Need in One Place
            </h2>
            <p className="text-gray-400 text-lg">
              Powerful features designed to streamline your workflow and boost productivity
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                title: "Smart Task Management",
                desc: "AI-powered task organization with intelligent suggestions and prioritization",
                icon: "📋"
              },
              {
                title: "Team Collaboration",
                desc: "Real-time collaboration tools that keep your team aligned and productive",
                icon: "👥"
              },
              {
                title: "Analytics Dashboard",
                desc: "Detailed insights into your productivity patterns and project progress",
                icon: "📊"
              },
              {
                title: "Cross-Platform Sync",
                desc: "Seamless synchronization across all your devices and platforms",
                icon: "🔄"
              },
              {
                title: "Custom Workflows",
                desc: "Create personalized workflows that match your team's unique processes",
                icon: "⚙️"
              },
              {
                title: "Secure & Private",
                desc: "Enterprise-grade security to keep your data safe and private",
                icon: "🔒"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index, duration: 0.5 }}
                className="p-6 card group hover:shadow-xl transition-all duration-300 border border-gray-700/50"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="relative z-10 py-20">
        <div className="container mx-auto px-6">
          <motion.div
            className="text-center mb-16 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              Trusted by Industry Leaders
            </h2>
            <p className="text-gray-400 text-lg">
              Join thousands of teams who transformed their workflow with FlowTask
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                quote: "FlowTask has revolutionized how our team manages projects. We've seen a 40% increase in productivity since implementation.",
                author: "Alex Johnson",
                role: "CTO, Tech Innovations"
              },
              {
                quote: "The intuitive interface and powerful features make it easy to stay organized and focused on what matters.",
                author: "Maria Garcia",
                role: "Product Manager, Global Solutions"
              },
              {
                quote: "I've tried many task management tools, but FlowTask is by far the most efficient and user-friendly.",
                author: "David Chen",
                role: "Operations Director, Enterprise Inc"
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 * index, duration: 0.5 }}
                className="p-6 card group hover:shadow-xl transition-all duration-300 border border-gray-700/50"
              >
                <div className="text-yellow-400 text-xl mb-4">★★★★★</div>
                <p className="text-gray-300 italic mb-6">"{testimonial.quote}"</p>
                <div>
                  <div className="font-semibold text-white">{testimonial.author}</div>
                  <div className="text-gray-500 text-sm">{testimonial.role}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-20">
        <div className="container mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl mx-auto p-8 md:p-12 card relative overflow-hidden border border-gray-700/50 text-center"
          >
            <div className="absolute -top-20 -right-20 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute -bottom-20 -left-20 w-64 h-64 bg-purple-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
            <div className="relative z-10">
              <h2 className="text-3xl md:text-4xl font-bold mb-6 bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                Ready to Transform Your Workflow?
              </h2>
              <p className="text-gray-300 mb-8 text-lg max-w-2xl mx-auto">
                Join thousands of professionals who have streamlined their workflow and increased productivity.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSignupClick}
                  className="btn btn-primary px-8 py-4 rounded-xl text-lg font-semibold transition-all duration-300"
                >
                  Start Free Trial
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleLoginClick}
                  className="btn btn-outline px-8 py-4 rounded-xl text-lg font-medium transition-all duration-300"
                >
                  Sign In
                </motion.button>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 px-6 py-8 text-center text-gray-500 text-sm">
        <p>© 2025 FlowTask. Streamlined productivity for modern professionals.</p>
      </footer>

      {/* Floating Chat Widget */}
      <FloatingChatWidget />
    </div>
  );
}