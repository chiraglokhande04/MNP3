/** @type {import('tailwindcss').Config} */
export default {
	darkMode: ["class"],
	content: [
	  "./index.html",
	  "./src/**/*.{js,ts,jsx,tsx}",
	  "./node_modules/@shadcn/ui/dist/**/*.{js,ts,jsx,tsx}",
	],
	theme: {
	  extend: {
		borderRadius: {
		  lg: 'var(--radius)',
		  md: 'calc(var(--radius) - 2px)',
		  sm: 'calc(var(--radius) - 4px)',
		},
		colors: {
		  background: 'hsl(var(--background))',
		  foreground: 'hsl(var(--foreground))',
		  card: {
			DEFAULT: 'hsl(var(--card))',
			foreground: 'hsl(var(--card-foreground))',
		  },
		  popover: {
			DEFAULT: 'hsl(var(--popover))',
			foreground: 'hsl(var(--popover-foreground))',
		  },
		  primary: {
			DEFAULT: 'hsl(var(--primary))',
			foreground: 'hsl(var(--primary-foreground))',
		  },
		  secondary: {
			DEFAULT: 'hsl(var(--secondary))',
			foreground: 'hsl(var(--secondary-foreground))',
		  },
		  muted: {
			DEFAULT: 'hsl(var(--muted))',
			foreground: 'hsl(var(--muted-foreground))',
		  },
		  accent: {
			DEFAULT: 'hsl(var(--accent))',
			foreground: 'hsl(var(--accent-foreground))',
		  },
		  destructive: {
			DEFAULT: 'hsl(var(--destructive))',
			foreground: 'hsl(var(--destructive-foreground))',
		  },
		  border: 'hsl(var(--border))',
		  input: 'hsl(var(--input))',
		  ring: 'hsl(var(--ring))',
		  chart: {
			'1': 'hsl(var(--chart-1))',
			'2': 'hsl(var(--chart-2))',
			'3': 'hsl(var(--chart-3))',
			'4': 'hsl(var(--chart-4))',
			'5': 'hsl(var(--chart-5))',
		  },
		},
		keyframes: {
			fadeInUp: {
			  '0%': { opacity: 0, transform: 'translateY(20px)' },
			  '100%': { opacity: 1, transform: 'translateY(0)' },
			},
			slideInLeft: {
			  '0%': { opacity: 0, transform: 'translateX(-50px)' },
			  '100%': { opacity: 1, transform: 'translateX(0)' },
			},
			slideInUp: {
			  '0%': { opacity: 0, transform: 'translateY(50px)' },
			  '100%': { opacity: 1, transform: 'translateY(0)' },
			},
			slideInRight: {
			  '0%': { opacity: 0, transform: 'translateX(50px)' },
			  '100%': { opacity: 1, transform: 'translateX(0)' },
			},
		},
		animation: {
			fadeInUp: 'fadeInUp 0.8s ease-out forwards',
			slideInLeft: 'slideInLeft 0.8s ease-out forwards',
			slideInUp: 'slideInUp 0.8s ease-out forwards',
			slideInRight: 'slideInRight 0.8s ease-out forwards',
		  },
	  },
	},
	plugins: [require("tailwindcss-animate")],
  };
