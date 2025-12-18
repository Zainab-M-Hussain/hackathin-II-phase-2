"use client";

import { useRouter, usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import DarkModeToggle from "@/app/components/DarkModeToggle";
import MenuIcon from "@/app/components/icons/MenuIcon";
import CloseIcon from "@/app/components/icons/CloseIcon";

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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-emerald-900/20 to-black text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/3 left-1/4 w-[600px] h-[600px] bg-emerald-500/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/4 -right-1/4 w-[500px] h-[500px] bg-yellow-500/5 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute bottom-1/4 left-1/3 w-[400px] h-[400px] bg-gray-500/5 rounded-full blur-3xl animate-pulse delay-2000"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-20 px-6 py-6">
        <div className="container mx-auto flex justify-between items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-yellow-400 bg-clip-text text-transparent"
          >
            TaskMastery
          </motion.div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-6">
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
              className="px-4 py-2 rounded-lg bg-gray-800/50 hover:bg-emerald-600/20 border border-gray-700 hover:border-emerald-500/50 transition-all duration-300 font-medium"
            >
              Login
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSignupClick}
              className="px-4 py-2 rounded-lg bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 transition-all duration-300 font-medium shadow-lg hover:shadow-emerald-500/25"
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
            className="text-2xl px-6 py-3 rounded-lg bg-gray-800/50 hover:bg-emerald-600/20 border border-gray-700 hover:border-emerald-500/50 transition-all duration-300 font-medium"
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
            className="text-2xl px-6 py-3 rounded-lg bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 transition-all duration-300 font-medium shadow-lg hover:shadow-emerald-500/25"
          >
            Sign Up
          </motion.button>
          <div className="mt-4">
            <DarkModeToggle />
          </div>
        </motion.div>
      )}

      {/* Hero Section */}
      <main className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] px-6">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-5xl mx-auto"
        >
          <motion.h1
            className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 leading-tight"
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
          >
            <span className="bg-gradient-to-r from-emerald-400 via-yellow-400 to-emerald-400 bg-clip-text text-transparent">
              MASTER
            </span>
            <br />
            <span className="text-white">YOUR TASKS</span>
          </motion.h1>

          <motion.p
            className="text-xl md:text-2xl text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.8 }}
          >
            Transform your productivity with our cutting-edge task management platform.
            Built for professionals who demand precision, control, and elegance.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6"
          >
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleLoginClick}
              className="group relative px-8 py-4 bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 rounded-xl text-lg font-semibold overflow-hidden transition-all duration-300 shadow-lg hover:shadow-emerald-500/25 min-w-[200px]"
            >
              <span className="relative z-10">Access Dashboard</span>
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-700 to-emerald-800 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              <div className="absolute inset-0 bg-emerald-500 transform scale-x-0 group-hover:scale-x-100 origin-left transition-transform duration-300"></div>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSignupClick}
              className="px-8 py-4 rounded-xl font-semibold border-2 border-emerald-500 text-emerald-400 hover:bg-emerald-500/10 transition-all duration-300 min-w-[200px]"
            >
              Get Started
            </motion.button>
          </motion.div>

          <motion.p
            className="mt-6 text-gray-400 text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.8 }}
          >
            Join thousands of professionals transforming their productivity
          </motion.p>
        </motion.div>
      </main>

      {/* Features Section */}
      <section className="relative z-10 py-20">
        <div className="container mx-auto px-6">
          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto"
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1, duration: 0.8 }}
          >
            {[
              {
                title: "Smart Organization",
                desc: "Intelligent task categorization and prioritization with AI-powered suggestions",
                icon: "🧠"
              },
              {
                title: "Real-time Sync",
                desc: "Instant updates across all your devices with seamless synchronization",
                icon: "🔄"
              },
              {
                title: "Advanced Analytics",
                desc: "Detailed insights into your productivity patterns and task completion rates",
                icon: "📊"
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 1.2 + index * 0.1, duration: 0.5 }}
                className="p-8 bg-gray-800/30 backdrop-blur-sm border border-gray-700/50 rounded-2xl hover:border-emerald-500/30 transition-all duration-300 hover:transform hover:-translate-y-2"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-emerald-400 mb-3">{feature.title}</h3>
                <p className="text-gray-300">{feature.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 py-20">
        <div className="container mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.5, duration: 0.8 }}
            className="max-w-3xl mx-auto p-12 bg-gradient-to-r from-gray-800/50 to-gray-900/50 backdrop-blur-sm rounded-3xl border border-gray-700/50"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6 bg-gradient-to-r from-emerald-400 to-yellow-400 bg-clip-text text-transparent">
              Ready to Transform Your Productivity?
            </h2>
            <p className="text-gray-300 mb-8 text-lg">
              Join thousands of professionals who have revolutionized their task management workflow.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleSignupClick}
                className="px-8 py-4 bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 rounded-xl text-lg font-semibold transition-all duration-300 shadow-lg hover:shadow-emerald-500/25"
              >
                Start Free Trial
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleLoginClick}
                className="px-8 py-4 rounded-xl font-medium border border-gray-600 hover:bg-gray-700/50 transition-all duration-300"
              >
                Sign In
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 px-6 py-8 text-center text-gray-500 text-sm">
        <p>© 2025 TaskMastery. Precision tools for productive minds.</p>
      </footer>
    </div>
  );
}