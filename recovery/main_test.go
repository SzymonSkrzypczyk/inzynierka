package main

import "testing"

func TestParseArgs(t *testing.T) {
	tests := []struct {
		name string
		args []string
		want string
		fail bool
	}{
		{name: "all archives", want: ""},
		{name: "one date", args: []string{"--date", "2026-01-22"}, want: "2026-01-22"},
		{name: "invalid date", args: []string{"--date", "22-01-2026"}, fail: true},
		{name: "missing date", args: []string{"--date"}, fail: true},
		{name: "unexpected argument", args: []string{"2026-01-22"}, fail: true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := parseArgs(tt.args)
			if (err != nil) != tt.fail {
				t.Fatalf("parseArgs(%v) error = %v, fail = %v", tt.args, err, tt.fail)
			}
			if got != tt.want {
				t.Fatalf("parseArgs(%v) = %q, want %q", tt.args, got, tt.want)
			}
		})
	}
}
